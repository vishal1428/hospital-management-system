from django.db import models

from shortuuid.django_fields import ShortUUIDField

from doctor import models as doctor_models
from patient import models as patient_models

class Service(models.Model):
    image = models.FileField(upload_to="images", null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available_doctors = models.ManyToManyField(doctor_models.Doctor, blank=True)

    def __str__(self):
        return f"{self.name} - {self.cost:.2f}"
    


class Appointment(models.Model):
    STATUS = [
        ('Scheduled', 'Scheduled'), 
        ('Completed', 'Completed'), 
        ('Pending', 'Pending'), 
        ('Cancelled', 'Cancelled')
    ]
    
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_appointments')
    doctor = models.ForeignKey(doctor_models.Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_appointments')
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_patient')
    appointment_date = models.DateTimeField(null=True, blank=True)
    issues = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    appointment_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")
    status = models.CharField(max_length=120, choices=STATUS)

    def __str__(self):
        patient_name = self.patient.full_name if self.patient and self.patient.full_name else "Unknown Patient"
        doctor_name = self.doctor.full_name if self.doctor and self.doctor.full_name else "Unknown Doctor"
        return f"{patient_name} with {doctor_name}"
    


class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()

    def __str__(self):
        patient_name = self.appointment.patient.full_name if self.appointment and self.appointment.patient and self.appointment.patient.full_name else "Unknown Patient"
        return f"Medical Record for {patient_name}"


class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.test_name}"


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medications = models.TextField(blank=True, null=True)

    def __str__(self):
        patient_name = self.appointment.patient.full_name if self.appointment and self.appointment.patient and self.appointment.patient.full_name else "Unknown Patient"
        return f"Prescription for {patient_name}"
    

class Billing(models.Model):
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True, blank=True,  related_name='billings')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='billing', blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)  # Deprecated: VAT/tax is no longer used, always zero
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=120, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        patient_name = self.patient.full_name if self.patient and self.patient.full_name else "Unknown Patient"
        return f"Billing for {patient_name} - Total: {self.total}"

