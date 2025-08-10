from django.core.management.base import BaseCommand
from doctor import models as doctor_models
import random

class Command(BaseCommand):
    help = 'Update existing doctors with realistic bios'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting doctor bio updates...'))
        
        doctors = doctor_models.Doctor.objects.all()
        
        if not doctors:
            self.stdout.write(self.style.ERROR('No doctors found.'))
            return
        
        updated_count = 0
        
        for doctor in doctors:
            specialization = doctor.specialization or "General Medicine"
            experience_years = int(doctor.years_of_experience) if doctor.years_of_experience and doctor.years_of_experience.isdigit() else 10
            
            new_bio = self.generate_doctor_bio(specialization, experience_years)
            doctor.bio = new_bio
            doctor.save()
            
            self.stdout.write(f'Updated bio for {doctor.full_name}: {new_bio[:50]}...')
            updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} doctors!'))
    
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