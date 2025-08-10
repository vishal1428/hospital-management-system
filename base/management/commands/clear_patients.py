from django.core.management.base import BaseCommand
from patient import models as patient_models
from userauths import models as userauths_models

class Command(BaseCommand):
    help = 'Clear only patient data created by populate_data command'

    def handle(self, *args, **options):
        self.stdout.write('Starting to clear patient data...')
        
        # Get all patients
        patients = patient_models.Patient.objects.all()
        patient_count = patients.count()
        
        if patient_count == 0:
            self.stdout.write('No patients found to delete.')
            return
        
        # Get their user accounts
        patient_users = [patient.user for patient in patients]
        
        # Delete patients first
        patients.delete()
        self.stdout.write(f'Deleted {patient_count} patients')
        
        # Delete their user accounts (but not superusers)
        deleted_users = 0
        for user in patient_users:
            if not user.is_superuser:
                user.delete()
                deleted_users += 1
        
        self.stdout.write(f'Deleted {deleted_users} patient user accounts')
        self.stdout.write(self.style.SUCCESS('Successfully cleared patient data!')) 