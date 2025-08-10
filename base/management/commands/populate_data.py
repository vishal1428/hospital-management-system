from django.core.management.base import BaseCommand
from userauths.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
import os
from faker import Faker
from base import models as base_models
from doctor import models as doctor_models
from patient import models as patient_models
import random
from datetime import datetime, timedelta

fake = Faker(['en_IN'])

class Command(BaseCommand):
    help = 'Populate database with comprehensive Indian hospital data including images'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Create services with images
        self.create_services()
        
        # Create doctors with profile images
        self.create_doctors()
        
        # Create patients
        self.create_patients()
        
        # Create appointments
        self.create_appointments()
        
        # Create medical records
        self.create_medical_records()
        
        # Create billings
        self.create_billings()
        
        # Create notifications
        self.create_notifications()
        
        self.stdout.write(self.style.SUCCESS('Data population completed successfully!'))

    def download_image(self, url, filename):
        """Download image from URL and return file path"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Create media directory if it doesn't exist
                media_dir = 'media/images'
                os.makedirs(media_dir, exist_ok=True)
                
                file_path = os.path.join(media_dir, filename)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return file_path
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to download image {url}: {e}'))
        return None

    def create_services(self):
        """Create services with images"""
        self.stdout.write('Creating services...')
        
        services_data = [
            {
                'name': 'Cardiology',
                'description': 'Comprehensive heart care including diagnosis, treatment, and prevention of cardiovascular diseases.',
                'cost': 2500.00,
                'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=500&h=300&fit=crop',
                'filename': 'cardiology.jpg'
            },
            {
                'name': 'Neurology',
                'description': 'Specialized care for disorders of the nervous system including brain and spinal cord.',
                'cost': 3000.00,
                'image_url': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=500&h=300&fit=crop',
                'filename': 'neurology.jpg'
            },
            {
                'name': 'Orthopedics',
                'description': 'Treatment of musculoskeletal system including bones, joints, muscles, and ligaments.',
                'cost': 2000.00,
                'image_url': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=500&h=300&fit=crop',
                'filename': 'orthopedics.jpg'
            },
            {
                'name': 'Dermatology',
                'description': 'Diagnosis and treatment of skin, hair, and nail conditions.',
                'cost': 1500.00,
                'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=500&h=300&fit=crop',
                'filename': 'dermatology.jpg'
            },
            {
                'name': 'Pediatrics',
                'description': 'Comprehensive healthcare for infants, children, and adolescents.',
                'cost': 1800.00,
                'image_url': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=500&h=300&fit=crop',
                'filename': 'pediatrics.jpg'
            },
            {
                'name': 'Ophthalmology',
                'description': 'Eye care including diagnosis and treatment of eye diseases and vision problems.',
                'cost': 2200.00,
                'image_url': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=500&h=300&fit=crop',
                'filename': 'ophthalmology.jpg'
            },
            {
                'name': 'ENT (Ear, Nose, Throat)',
                'description': 'Specialized care for ear, nose, throat, and related head and neck conditions.',
                'cost': 1900.00,
                'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=500&h=300&fit=crop',
                'filename': 'ent.jpg'
            },
            {
                'name': 'Gastroenterology',
                'description': 'Diagnosis and treatment of digestive system disorders.',
                'cost': 2400.00,
                'image_url': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=500&h=300&fit=crop',
                'filename': 'gastroenterology.jpg'
            },
            {
                'name': 'Urology',
                'description': 'Treatment of urinary tract and male reproductive system disorders.',
                'cost': 2600.00,
                'image_url': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=500&h=300&fit=crop',
                'filename': 'urology.jpg'
            },
            {
                'name': 'Psychiatry',
                'description': 'Mental health care including diagnosis and treatment of psychiatric disorders.',
                'cost': 2800.00,
                'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=500&h=300&fit=crop',
                'filename': 'psychiatry.jpg'
            },
            {
                'name': 'Oncology',
                'description': 'Cancer diagnosis, treatment, and management.',
                'cost': 3500.00,
                'image_url': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=500&h=300&fit=crop',
                'filename': 'oncology.jpg'
            },
            {
                'name': 'Radiology',
                'description': 'Medical imaging and diagnostic radiology services.',
                'cost': 2100.00,
                'image_url': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=500&h=300&fit=crop',
                'filename': 'radiology.jpg'
            }
        ]
        
        for service_data in services_data:
            service, created = base_models.Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'description': service_data['description'],
                    'cost': service_data['cost']
                }
            )
            
            if created or not service.image:
                # Download image
                image_path = self.download_image(service_data['image_url'], service_data['filename'])
                if image_path:
                    with open(image_path, 'rb') as img_file:
                        service.image.save(service_data['filename'], File(img_file), save=True)
                    self.stdout.write(f'Created service: {service.name} with image')
                else:
                    self.stdout.write(f'Created service: {service.name} (no image)')
            else:
                self.stdout.write(f'Service already exists: {service.name}')

    def create_doctors(self):
        """Create doctors with profile images"""
        self.stdout.write('Creating doctors...')
        
        # Get all services for assignment
        services = list(base_models.Service.objects.all())
        
        # Doctor profile image URLs
        doctor_images = [
            'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&h=300&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=300&h=300&fit=crop&crop=face',
        ]
        
        created_doctors = []
        
        for i in range(20):  # Create 20 doctors
            # Generate Indian name
            first_name = fake.first_name_male() if i % 2 == 0 else fake.first_name_female()
            last_name = fake.last_name()
            full_name = f"Dr. {first_name} {last_name}"
            
            # Create user
            username = f"doctor_{i+1}"
            email = f"doctor{i+1}@hospital.com"
            
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'user_type': 'Doctor',
                    'is_staff': True
                }
            )
            
            if created:
                user.set_password('doctor123')
                user.save()
            
            # Create doctor profile
            specialization = random.choice(services).name  # <-- define it here
            doctor, created = doctor_models.Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': full_name,
                    'specialization': specialization,  # use it here
                    'qualifications': random.choice(['MBBS, MD', 'MBBS, MS', 'MBBS, DNB', 'MBBS, FRCS']),
                    'years_of_experience': str(random.randint(5, 25)),
                    'mobile': fake.phone_number(),
                    'country': 'India',
                    'bio': self.generate_doctor_bio(specialization, random.randint(5, 25))
                }
            )
            
            # Add profile image
            if created or not doctor.image:
                image_url = doctor_images[i % len(doctor_images)]
                image_path = self.download_image(image_url, f"doctor_{i+1}.jpg")
                if image_path:
                    with open(image_path, 'rb') as img_file:
                        doctor.image.save(f"doctor_{i+1}.jpg", File(img_file), save=True)
                    self.stdout.write(f'Created doctor: {doctor.full_name} with image')
                else:
                    self.stdout.write(f'Created doctor: {doctor.full_name} (no image)')
            else:
                self.stdout.write(f'Doctor already exists: {doctor.full_name}')
            
            created_doctors.append(doctor)
        
        # Assign doctors to services based on their specialization
        self.assign_doctors_to_services(created_doctors, services)
    
    def assign_doctors_to_services(self, doctors, services):
        """Assign doctors to services based on their specialization"""
        self.stdout.write('Assigning doctors to services...')
        
        # Create a mapping of specializations to services
        specialization_mapping = {
            'Cardiology': ['Cardiology'],
            'Neurology': ['Neurology'],
            'Orthopedics': ['Orthopedics'],
            'Dermatology': ['Dermatology'],
            'Pediatrics': ['Pediatrics'],
            'Ophthalmology': ['Ophthalmology'],
            'ENT (Ear, Nose, Throat)': ['ENT (Ear, Nose, Throat)'],
            'Gastroenterology': ['Gastroenterology'],
            'Urology': ['Urology'],
            'Psychiatry': ['Psychiatry'],
            'Oncology': ['Oncology'],
            'Radiology': ['Radiology']
        }
        
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
            additional_services = random.sample([s for s in services if s not in matching_services], 
                                             min(2, len(services) - len(matching_services)))
            for service in additional_services:
                service.available_doctors.add(doctor)
                self.stdout.write(f'Assigned {doctor.full_name} to additional service: {service.name}')

    def create_patients(self):
        """Create patients"""
        self.stdout.write('Creating patients...')
        
        for i in range(50):  # Create 50 patients
            # Generate Indian name
            first_name = fake.first_name_male() if i % 2 == 0 else fake.first_name_female()
            last_name = fake.last_name()
            full_name = f"{first_name} {last_name}"
            
            # Create user
            username = f"patient_{i+1}"
            email = f"patient{i+1}@email.com"
            
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'user_type': 'Patient'
                }
            )
            
            if created:
                user.set_password('patient123')
                user.save()
            
            # Create patient profile
            patient, created = patient_models.Patient.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': full_name,
                    'email': email,
                    'mobile': fake.phone_number(),
                    'address': fake.address(),
                    'gender': random.choice(['Male', 'Female']),
                    'dob': fake.date_of_birth(minimum_age=18, maximum_age=80),
                    'blood_group': random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
                }
            )
            
            if created:
                self.stdout.write(f'Created patient: {patient.full_name}')
            else:
                self.stdout.write(f'Patient already exists: {patient.full_name}')

    def create_appointments(self):
        """Create appointments"""
        self.stdout.write('Creating appointments...')
        
        doctors = list(doctor_models.Doctor.objects.all())
        patients = list(patient_models.Patient.objects.all())
        services = list(base_models.Service.objects.all())
        
        statuses = ['Scheduled', 'Completed', 'Cancelled', 'Pending']
        
        for i in range(100):  # Create 100 appointments
            doctor = random.choice(doctors)
            patient = random.choice(patients)
            service = random.choice(services)
            
            # Generate appointment date (within last 30 days to next 30 days)
            appointment_date = fake.date_time_between(start_date='-30d', end_date='+30d')
            
            appointment, created = base_models.Appointment.objects.get_or_create(
                doctor=doctor,
                patient=patient,
                service=service,
                appointment_date=appointment_date,
                defaults={
                    'status': random.choice(statuses),
                    'symptoms': fake.text(max_nb_chars=200),
                    'issues': fake.text(max_nb_chars=200)
                }
            )
            
            if created:
                self.stdout.write(f'Created appointment: {patient.full_name} with Dr. {doctor.full_name}')

    def create_medical_records(self):
        """Create medical records"""
        self.stdout.write('Creating medical records...')
        
        appointments = list(base_models.Appointment.objects.filter(status='Completed'))
        
        diagnoses = [
            'Hypertension', 'Diabetes Type 2', 'Asthma', 'Migraine', 'Arthritis',
            'Gastritis', 'Sinusitis', 'Bronchitis', 'Urinary Tract Infection',
            'Anxiety Disorder', 'Depression', 'Insomnia', 'Obesity', 'Anemia'
        ]
        
        treatments = [
            'Medication therapy', 'Physical therapy', 'Lifestyle modifications',
            'Surgical intervention', 'Counseling', 'Dietary changes',
            'Exercise program', 'Stress management', 'Regular monitoring'
        ]
        
        for appointment in appointments[:50]:  # Create records for 50 completed appointments
            record, created = base_models.MedicalRecord.objects.get_or_create(
                appointment=appointment,
                defaults={
                    'diagnosis': random.choice(diagnoses),
                    'treatment': random.choice(treatments)
                }
            )
            
            if created:
                self.stdout.write(f'Created medical record for: {appointment.patient.full_name}')

    def create_billings(self):
        """Create billings"""
        self.stdout.write('Creating billings...')
        
        appointments = list(base_models.Appointment.objects.all())
        
        for appointment in appointments[:80]:  # Create billings for 80 appointments
            sub_total = float(appointment.service.cost) + random.randint(500, 2000)
            tax = 0.00  # Tax is always 0 as per model comment
            total = sub_total
            
            billing, created = base_models.Billing.objects.get_or_create(
                appointment=appointment,
                defaults={
                    'patient': appointment.patient,
                    'sub_total': sub_total,
                    'tax': tax,
                    'total': total,
                    'status': random.choice(['Paid', 'Unpaid'])
                }
            )
            
            if created:
                self.stdout.write(f'Created billing for: {appointment.patient.full_name} - ₹{total}')

    def create_notifications(self):
        """Create notifications"""
        self.stdout.write('Creating notifications...')
        
        doctors = list(doctor_models.Doctor.objects.all())
        patients = list(patient_models.Patient.objects.all())
        appointments = list(base_models.Appointment.objects.all())
        
        # Doctor notifications
        for doctor in doctors:
            for i in range(random.randint(2, 5)):
                appointment = random.choice(appointments) if appointments else None
                notification, created = doctor_models.Notification.objects.get_or_create(
                    doctor=doctor,
                    appointment=appointment,
                    type=random.choice(['New Appointment', 'Appointment Cancelled']),
                    defaults={
                        'seen': random.choice([True, False])
                    }
                )
        
        # Patient notifications
        for patient in patients:
            for i in range(random.randint(1, 3)):
                appointment = random.choice(appointments) if appointments else None
                notification, created = patient_models.Notification.objects.get_or_create(
                    patient=patient,
                    appointment=appointment,
                    type=random.choice(['Appointment Scheduled', 'Appointment Cancelled']),
                    defaults={
                        'seen': random.choice([True, False])
                    }
                )
        
        self.stdout.write('Created notifications for doctors and patients')
    
    def generate_doctor_bio(self, specialization, experience_years):
        """Generate realistic doctor bio based on specialization and experience"""
        bios = {
            'Cardiology': [
                f"Experienced cardiologist with {experience_years} years of practice specializing in heart disease diagnosis and treatment. Expert in interventional cardiology and preventive cardiology.",
                f"Senior cardiologist with {experience_years} years of experience in treating cardiovascular diseases. Specializes in echocardiography and cardiac catheterization.",
                f"Board-certified cardiologist with {experience_years} years of clinical experience. Expert in managing heart failure, arrhythmias, and coronary artery disease."
            ],
            'Neurology': [
                f"Neurologist with {experience_years} years of experience in treating neurological disorders. Specializes in stroke management and epilepsy treatment.",
                f"Senior neurologist with {experience_years} years of practice. Expert in movement disorders, multiple sclerosis, and neuroimaging.",
                f"Board-certified neurologist with {experience_years} years of clinical experience. Specializes in headache disorders and neuromuscular diseases."
            ],
            'Orthopedics': [
                f"Orthopedic surgeon with {experience_years} years of experience in joint replacement and sports medicine. Expert in arthroscopic surgery.",
                f"Senior orthopedic specialist with {experience_years} years of practice. Specializes in spine surgery and trauma care.",
                f"Board-certified orthopedic surgeon with {experience_years} years of experience. Expert in pediatric orthopedics and fracture management."
            ],
            'Dermatology': [
                f"Dermatologist with {experience_years} years of experience in medical and cosmetic dermatology. Expert in skin cancer screening and treatment.",
                f"Senior dermatologist with {experience_years} years of practice. Specializes in psoriasis, eczema, and laser treatments.",
                f"Board-certified dermatologist with {experience_years} years of experience. Expert in Mohs surgery and aesthetic procedures."
            ],
            'Pediatrics': [
                f"Pediatrician with {experience_years} years of experience in child healthcare. Specializes in newborn care and childhood vaccinations.",
                f"Senior pediatrician with {experience_years} years of practice. Expert in childhood development and behavioral pediatrics.",
                f"Board-certified pediatrician with {experience_years} years of experience. Specializes in pediatric emergency care and adolescent medicine."
            ],
            'Ophthalmology': [
                f"Ophthalmologist with {experience_years} years of experience in eye care. Specializes in cataract surgery and retinal disorders.",
                f"Senior ophthalmologist with {experience_years} years of practice. Expert in glaucoma treatment and corneal surgery.",
                f"Board-certified ophthalmologist with {experience_years} years of experience. Specializes in pediatric ophthalmology and oculoplastic surgery."
            ],
            'ENT (Ear, Nose, Throat)': [
                f"ENT specialist with {experience_years} years of experience in head and neck surgery. Expert in hearing disorders and sinus surgery.",
                f"Senior ENT surgeon with {experience_years} years of practice. Specializes in voice disorders and sleep apnea treatment.",
                f"Board-certified ENT specialist with {experience_years} years of experience. Expert in pediatric ENT and skull base surgery."
            ],
            'Gastroenterology': [
                f"Gastroenterologist with {experience_years} years of experience in digestive disorders. Expert in endoscopy and colonoscopy procedures.",
                f"Senior gastroenterologist with {experience_years} years of practice. Specializes in inflammatory bowel disease and liver disorders.",
                f"Board-certified gastroenterologist with {experience_years} years of experience. Expert in pancreatic diseases and therapeutic endoscopy."
            ],
            'Urology': [
                f"Urologist with {experience_years} years of experience in urinary tract disorders. Expert in prostate surgery and kidney stone treatment.",
                f"Senior urologist with {experience_years} years of practice. Specializes in male infertility and urologic oncology.",
                f"Board-certified urologist with {experience_years} years of experience. Expert in robotic surgery and pediatric urology."
            ],
            'Psychiatry': [
                f"Psychiatrist with {experience_years} years of experience in mental health care. Specializes in mood disorders and anxiety treatment.",
                f"Senior psychiatrist with {experience_years} years of practice. Expert in child and adolescent psychiatry.",
                f"Board-certified psychiatrist with {experience_years} years of experience. Specializes in addiction medicine and geriatric psychiatry."
            ],
            'Oncology': [
                f"Oncologist with {experience_years} years of experience in cancer treatment. Specializes in chemotherapy and targeted therapy.",
                f"Senior oncologist with {experience_years} years of practice. Expert in radiation oncology and palliative care.",
                f"Board-certified oncologist with {experience_years} years of experience. Specializes in hematologic malignancies and immunotherapy."
            ],
            'Radiology': [
                f"Radiologist with {experience_years} years of experience in diagnostic imaging. Expert in MRI, CT, and ultrasound interpretation.",
                f"Senior radiologist with {experience_years} years of practice. Specializes in interventional radiology and nuclear medicine.",
                f"Board-certified radiologist with {experience_years} years of experience. Expert in pediatric radiology and musculoskeletal imaging."
            ]
        }
        
        # Get bio options for the specialization, or use a default if not found
        bio_options = bios.get(specialization, [
            f"Experienced {specialization.lower()} specialist with {experience_years} years of practice. Dedicated to providing high-quality patient care.",
            f"Senior {specialization.lower()} doctor with {experience_years} years of clinical experience. Committed to excellence in medical care.",
            f"Board-certified {specialization.lower()} specialist with {experience_years} years of experience. Focused on patient-centered care."
        ])
        
        return random.choice(bio_options) 