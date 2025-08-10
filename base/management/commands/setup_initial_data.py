from django.core.management.base import BaseCommand
from base.models import Service
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Set up initial data for the Hospital Management System'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial data...')
        
        # Create services if they don't exist
        services_data = [
            {
                'name': 'General Medicine',
                'description': 'Comprehensive medical care for adults and children',
                'cost': 500.00
            },
            {
                'name': 'Cardiology',
                'description': 'Specialized care for heart and cardiovascular conditions',
                'cost': 800.00
            },
            {
                'name': 'Orthopedics',
                'description': 'Treatment for bone, joint, and muscle conditions',
                'cost': 600.00
            },
            {
                'name': 'Dermatology',
                'description': 'Skin care and treatment for skin conditions',
                'cost': 400.00
            },
            {
                'name': 'Pediatrics',
                'description': 'Specialized medical care for children',
                'cost': 450.00
            }
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'Created service: {service.name}')
            else:
                self.stdout.write(f'Service already exists: {service.name}')
        
        self.stdout.write(self.style.SUCCESS('Initial data setup completed!')) 