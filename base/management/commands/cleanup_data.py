from django.core.management.base import BaseCommand
from django.db import models
from base import models as base_models
from doctor import models as doctor_models
from patient import models as patient_models

class Command(BaseCommand):
    help = 'Clean up orphaned data and fix null references'

    def handle(self, *args, **options):
        self.stdout.write('Starting data cleanup...')
        
        # Clean up appointments with null doctors or patients
        orphaned_appointments = base_models.Appointment.objects.filter(
            models.Q(doctor__isnull=True) | models.Q(patient__isnull=True)
        )
        
        if orphaned_appointments.exists():
            count = orphaned_appointments.count()
            self.stdout.write(f'Found {count} appointments with null doctor or patient references')
            
            # Delete orphaned appointments
            orphaned_appointments.delete()
            self.stdout.write(f'Deleted {count} orphaned appointments')
        else:
            self.stdout.write('No orphaned appointments found')
        
        # Clean up medical records with null appointments
        orphaned_medical_records = base_models.MedicalRecord.objects.filter(
            appointment__isnull=True
        )
        
        if orphaned_medical_records.exists():
            count = orphaned_medical_records.count()
            self.stdout.write(f'Found {count} medical records with null appointment references')
            orphaned_medical_records.delete()
            self.stdout.write(f'Deleted {count} orphaned medical records')
        else:
            self.stdout.write('No orphaned medical records found')
        
        # Clean up lab tests with null appointments
        orphaned_lab_tests = base_models.LabTest.objects.filter(
            appointment__isnull=True
        )
        
        if orphaned_lab_tests.exists():
            count = orphaned_lab_tests.count()
            self.stdout.write(f'Found {count} lab tests with null appointment references')
            orphaned_lab_tests.delete()
            self.stdout.write(f'Deleted {count} orphaned lab tests')
        else:
            self.stdout.write('No orphaned lab tests found')
        
        # Clean up prescriptions with null appointments
        orphaned_prescriptions = base_models.Prescription.objects.filter(
            appointment__isnull=True
        )
        
        if orphaned_prescriptions.exists():
            count = orphaned_prescriptions.count()
            self.stdout.write(f'Found {count} prescriptions with null appointment references')
            orphaned_prescriptions.delete()
            self.stdout.write(f'Deleted {count} orphaned prescriptions')
        else:
            self.stdout.write('No orphaned prescriptions found')
        
        # Clean up billing with null patients
        orphaned_billings = base_models.Billing.objects.filter(
            patient__isnull=True
        )
        
        if orphaned_billings.exists():
            count = orphaned_billings.count()
            self.stdout.write(f'Found {count} billings with null patient references')
            orphaned_billings.delete()
            self.stdout.write(f'Deleted {count} orphaned billings')
        else:
            self.stdout.write('No orphaned billings found')
        
        # Clean up doctor notifications with null doctors
        orphaned_doctor_notifications = doctor_models.Notification.objects.filter(
            doctor__isnull=True
        )
        
        if orphaned_doctor_notifications.exists():
            count = orphaned_doctor_notifications.count()
            self.stdout.write(f'Found {count} doctor notifications with null doctor references')
            orphaned_doctor_notifications.delete()
            self.stdout.write(f'Deleted {count} orphaned doctor notifications')
        else:
            self.stdout.write('No orphaned doctor notifications found')
        
        # Clean up patient notifications with null patients
        orphaned_patient_notifications = patient_models.Notification.objects.filter(
            patient__isnull=True
        )
        
        if orphaned_patient_notifications.exists():
            count = orphaned_patient_notifications.count()
            self.stdout.write(f'Found {count} patient notifications with null patient references')
            orphaned_patient_notifications.delete()
            self.stdout.write(f'Deleted {count} orphaned patient notifications')
        else:
            self.stdout.write('No orphaned patient notifications found')
        
        self.stdout.write(self.style.SUCCESS('Data cleanup completed successfully!')) 