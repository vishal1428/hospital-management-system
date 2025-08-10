from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import requests
# import stripe
try:
    import razorpay
except ImportError:
    razorpay = None


from base import models as base_models
from doctor import models as doctor_models
from patient import models as patient_models

def index(request):
    services = base_models.Service.objects.all()
    context = {
        "services": services
    }
    return render(request, "base/index.html", context)

def service_detail(request, service_id):
    service = base_models.Service.objects.get(id=service_id)

    context = {
        "service": service
    }
    return render(request, "base/service_detail.html", context)

@login_required
def book_appointment(request, service_id, doctor_id):
    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_models.Doctor.objects.get(id=doctor_id)
    patient = patient_models.Patient.objects.get(user=request.user)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        dob = request.POST.get("dob")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")

        # Validate required fields
        errors = []
        
        if not dob or not dob.strip():
            errors.append("Date of Birth is required.")
        
        if not issues or not issues.strip():
            errors.append("Please describe your health issues.")
            
        if not symptoms or not symptoms.strip():
            errors.append("Please describe your symptoms.")
        
        # If there are validation errors, show them and return to form
        if errors:
            for error in errors:
                messages.error(request, error)
            context = {
                "service": service,
                "doctor": doctor,
                "patient": patient,
            }
            return render(request, "base/book_appointment.html", context)

        # Update patient bio data
        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        # Only update dob if it's not empty
        if dob and dob.strip():
            patient.dob = dob
        patient.save()

        # Create appointment object
        appointment = base_models.Appointment.objects.create(
            service=service,
            doctor=doctor,
            patient=patient,
            appointment_date=doctor.next_available_appointment_date,
            issues=issues,
            symptoms=symptoms,
        )

        # Create a billing objects
        billing = base_models.Billing()
        billing.patient = patient
        billing.appointment = appointment
        billing.sub_total = appointment.service.cost
        billing.tax = 0
        billing.total = billing.sub_total
        billing.status = "Unpaid"
        billing.save()

        return redirect("base:checkout", billing.billing_id)

    context = {
        "service": service,
        "doctor": doctor,
        "patient": patient,
    }
    return render(request, "base/book_appointment.html", context)

@login_required
def checkout(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    
    if razorpay is None:
        # Fallback for deployment without razorpay
        context = {
            "billing": billing,
            "razorpay_key_id": "rzp_test_dummy",
            "razorpay_order_id": "order_dummy",
            "amount": int(billing.total * 100),
        }
        return render(request, "base/checkout.html", context)
    
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": int(billing.total * 100),  # INR in paise
        "currency": "INR",
        "receipt": f"receipt_{billing_id}",
        "payment_capture": 1
    })

    context = {
        "billing": billing,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "razorpay_order_id": payment['id'],
        "amount": payment['amount'],
    }

    return render(request, "base/checkout.html", context)


@csrf_exempt
@login_required
def razorpay_checkout(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    
    if razorpay is None:
        # Fallback for deployment without razorpay
        context = {
            "billing": billing,
            "razorpay_key_id": "rzp_test_dummy",
            "razorpay_order_id": "order_dummy",
            "amount": int(billing.total * 100),
        }
        return render(request, "base/checkout.html", context)
    
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": int(billing.total * 100),  # INR in paise
        "currency": "INR",
        "receipt": f"receipt_{billing_id}",
        "payment_capture": 1
    })

    context = {
        "billing": billing,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "razorpay_order_id": payment['id'],
        "amount": payment['amount'],
    }

    return render(request, "base/checkout.html", context)

@csrf_exempt
def razorpay_payment_verify(request):
    if request.method == "POST":
        print("POST data received:", request.POST) #debugging 
        
        if razorpay is None:
            # Fallback for deployment without razorpay
            billing_id = request.POST.get("billing_id")
            billing = base_models.Billing.objects.get(billing_id=billing_id)
            billing.status = "Paid"
            billing.save()
            billing.appointment.status = "Scheduled"
            billing.appointment.save()
            return JsonResponse({"status": "success"})
            
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature = request.POST.get("razorpay_signature")
        billing_id = request.POST.get("billing_id")

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        billing = base_models.Billing.objects.get(billing_id=billing_id)

        try:
            client.utility.verify_payment_signature(params_dict)

            # Update billing and appointment status
            if billing.status == "Unpaid":
                billing.status = "Paid"
                billing.save()
                billing.appointment.status = "Scheduled"
                billing.appointment.save()

                doctor_models.Notification.objects.create(
                    doctor=billing.appointment.doctor,
                    appointment=billing.appointment,
                    type="New Appointment"
                )

                patient_models.Notification.objects.create(
                    patient=billing.appointment.patient,
                    appointment=billing.appointment,
                    type="Appointment Scheduled"
                )

                try:
                    merge_data = {
                        "billing": billing
                    }

                    # Send appointment email to doctor
                    subject = "New Appointment"
                    text_body = render_to_string("email/new_appointment.txt", merge_data)
                    html_body = render_to_string("email/new_appointment.html", merge_data)

                    msg = EmailMultiAlternatives(
                        subject=subject,
                        from_email=settings.FROM_EMAIL,
                        to=[billing.appointment.doctor.user.email],
                        body=text_body
                    )
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()

                    
                    # Send appointment email to patient
                    subject = "Appointment Booked Successfully"
                    text_body = render_to_string("email/appointment_booked.txt", merge_data)
                    html_body = render_to_string("email/appointment_booked.html", merge_data)

                    msg = EmailMultiAlternatives(
                        subject=subject,
                        from_email=settings.FROM_EMAIL,
                        to=[billing.appointment.patient.email],
                        body=text_body
                    )
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()
                    
                except Exception as e:
                    print(f"Error sending email: {e}")

            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")

        except razorpay.errors.SignatureVerificationError:
            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")


# def stripe_payment(request, billing_id):
#     billing = base_models.Billing.objects.get(billing_id=billing_id)
#     stripe.api_key = settings.STRIPE_SECRET_KEY

#     checkout_session = stripe.checkout.Session.create(
#         customer_email=billing.patient.email,
#         payment_method_types=['card'],
#         line_items = [
#             {
#                 'price_data': {
#                     'currency': 'USD',
#                     'product_data': {
#                         'name': billing.patient.full_name
#                     },
#                     'unit_amount': int(billing.total * 100)
#                 },
#                 'quantity': 1
#             }
#         ],
#         mode='payment',
#         success_url = request.build_absolute_uri(reverse("base:stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}",
#         cancel_url=request.build_absolute_uri(reverse("base:stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}"
        
#     )
#     return JsonResponse({"sessionId": checkout_session.id})


# def stripe_payment_verify(request, billing_id):
#     billing = base_models.Billing.objects.get(billing_id=billing_id)
#     session_id = request.GET.get("session_id")
#     session = stripe.checkout.Session.retrieve(session_id)

#     if session.payment_status == "paid":
#         if billing.status == "Unpaid":
#             billing.status = "Paid"
#             billing.save()
#             billing.appointment.status = "Completed"
#             billing.appointment.save()

#             doctor_models.Notification.objects.create(
#                 doctor=billing.appointment.doctor,
#                 appointment=billing.appointment,
#                 type="New Appointment"
#             )

#             patient_models.Notification.objects.create(
#                 patient=billing.appointment.patient,
#                 appointment=billing.appointment,
#                 type="Appointment Scheduled"
#             )

#             return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
#     else:
#         return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")
    

# def get_paypal_access_token():
#     token_url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
#     data = {'grant_type': 'client_credentials'}
#     auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET_ID)
#     response = requests.post(token_url, data=data, auth=auth)

#     if response.status_code == 200:
#         print("Access Token: ", response.json()['access_token'])
#         return response.json()['access_token']
#     else:
#         raise Exception(f"Failed to get access token from PayPal. Status code: {response.status_code}")


# def paypal_payment_verify(request, billing_id):
#     billing = base_models.Billing.objects.get(billing_id=billing_id)

#     transaction_id = request.GET.get("transaction_id")
#     print("transaction_id ====", transaction_id)
#     paypal_api_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{transaction_id}"
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {get_paypal_access_token()}'
#     }

#     response = requests.get(paypal_api_url, headers=headers)
#     print("Response: ", response)
#     print("Response Status Code: ", response.status_code)

#     if response.status_code == 200:
#         paypal_order_data = response.json()
#         paypal_payment_status = paypal_order_data['status']

#         if paypal_payment_status == "COMPLETED":
#             if billing.status == "Unpaid":
#                 billing.status = "Paid"
#                 billing.save()
#                 billing.appointment.status = "Completed"
#                 billing.appointment.save()

#                 doctor_models.Notification.objects.create(
#                     doctor=billing.appointment.doctor,
#                     appointment=billing.appointment,
#                     type="New Appointment"
#                 )

#                 patient_models.Notification.objects.create(
#                     patient=billing.appointment.patient,
#                     appointment=billing.appointment,
#                     type="Appointment Scheduled"
#                 )

#                 merge_data = {
#                     "billing": billing
#                 }

#                 # Send appointment email to doctor
#                 subject = "New Appointment"
#                 text_body = render_to_string("email/new_appointment.txt", merge_data)
#                 html_body = render_to_string("email/new_appointment.html", merge_data)

#                 # Add the try-catch to gracefully handle the case where email cannot be sent
#                 try:
#                     msg = EmailMultiAlternatives(
#                         subject=subject,
#                         from_email=settings.FROM_EMAIL,
#                         to=[billing.appointment.doctor.user.email],
#                         body=text_body
#                     )
#                     msg.attach_alternative(html_body, "text/html")
#                     msg.send()

#                     # Send appointment booked email to patient
#                     subject = "Appointment Booked Successfully"
#                     text_body = render_to_string("email/appointment_booked.txt", merge_data)
#                     html_body = render_to_string("email/appointment_booked.html", merge_data)

#                     msg = EmailMultiAlternatives(
#                         subject=subject,
#                         from_email=settings.FROM_EMAIL,
#                         to=[billing.appointment.patient.email],
#                         body=text_body
#                     )
#                     msg.attach_alternative(html_body, "text/html")
#                     msg.send()
#                 except:
#                     print("Email cannot be sent now!")

#                 return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
        
#         return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")
        
    
#     return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")
    

@login_required
def payment_status(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get("payment_status")

    context = {
        "billing": billing,
        "payment_status": payment_status,
    }
    
    response = render(request, "base/payment_status.html", context)
    # Add cache-busting headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def about_page(request):
    return render(request, "base/pages/about.html")

def contact_page(request):
    return render(request, "base/pages/contact.html")

def privacy_policy_page(request):
    return render(request, "base/pages/privacy_policy.html")

def terms_conditions_page(request):
    return render(request, "base/pages/terms_conditions.html")
