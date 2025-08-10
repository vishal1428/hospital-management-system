from django.core.management.base import BaseCommand
from base import models as base_models
from doctor import models as doctor_models
import random

class Command(BaseCommand):
    help = 'Assign existing doctors to services'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting doctor assignment to services...'))
        
        # Get all doctors and services
        doctors = list(doctor_models.Doctor.objects.all())
        services = list(base_models.Service.objects.all())
        
        if not doctors:
            self.stdout.write(self.style.ERROR('No doctors found. Please create doctors first.'))
            return
        
        if not services:
            self.stdout.write(self.style.ERROR('No services found. Please create services first.'))
            return
        
        # Clear existing assignments
        for service in services:
            service.available_doctors.clear()
        
        # Assign doctors to services based on their specialization
        for doctor in doctors:
            # Get the doctor's specialization
            specialization = doctor.specialization
            
            # Find matching services
            matching_services = []
            for service in services:
                if service.name == specialization:
                    matching_services.append(service)
            
            # If no exact match, assign to a random service
            if not matching_services:
                matching_services = [random.choice(services)]
            
            # Assign doctor to matching services
            for service in matching_services:
                service.available_doctors.add(doctor)
                self.stdout.write(f'Assigned {doctor.full_name} to {service.name}')
            
            # Also assign to 1-2 additional random services for variety
            remaining_services = [s for s in services if s not in matching_services]
            if remaining_services:
                additional_services = random.sample(remaining_services, 
                                                 min(2, len(remaining_services)))
                for service in additional_services:
                    service.available_doctors.add(doctor)
                    self.stdout.write(f'Assigned {doctor.full_name} to additional service: {service.name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully assigned doctors to services!'))
        
        # Show summary
        for service in services:
            doctor_count = service.available_doctors.count()
            self.stdout.write(f'{service.name}: {doctor_count} doctors') 