from django.urls import path
from base import views

app_name = "base"

urlpatterns = [
    path("", views.index, name="index"),
    path("service/<service_id>/", views.service_detail, name="service_detail"),
    path("book-appointment/<service_id>/<doctor_id>/", views.book_appointment, name="book_appointment"),
    path("checkout/<billing_id>/", views.checkout, name="checkout"),
    path("payment_status/<billing_id>/", views.payment_status, name="payment_status"),

    # path("stripe_payment/<billing_id>/", views.stripe_payment, name="stripe_payment"),
    # path("stripe_payment_verify/<billing_id>/", views.stripe_payment_verify, name="stripe_payment_verify"),
    # path("paypal_payment_verify/<billing_id>/", views.paypal_payment_verify, name="paypal_payment_verify"),

    path("razorpay_checkout/<str:billing_id>/", views.razorpay_checkout, name="razorpay_checkout"),
    path("razorpay_payment_verify/", views.razorpay_payment_verify, name="razorpay_payment_verify"),

    # Only keep these two static page URLs
    path("pages/about-us.html", views.about_page, name="about_us_html"),
    path("pages/contact-us.html", views.contact_page, name="contact_us_html"),
    path("pages/privacy-policy.html", views.privacy_policy_page, name="privacy_policy_html"),
    path("pages/terms-conditions.html", views.terms_conditions_page, name="terms_conditions_html"),

]