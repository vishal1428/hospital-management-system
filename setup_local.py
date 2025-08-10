#!/usr/bin/env python
"""
Setup script for Hospital Management System - Local Development
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return False

def setup_local():
    """Setup the Hospital Management System for local development"""
    print("🏥 Setting up Hospital Management System for Local Development")
    print("=" * 60)
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("📦 Creating virtual environment...")
        if not run_command("python -m venv venv"):
            print("❌ Failed to create virtual environment")
            return False
    
    # Activate virtual environment and install dependencies
    print("📦 Installing dependencies...")
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    if not run_command(f"{pip_cmd} install -r requirements.txt"):
        print("❌ Failed to install dependencies")
        return False
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS_prj.settings')
    
    try:
        django.setup()
    except Exception as e:
        print(f"❌ Failed to setup Django: {e}")
        return False
    
    # Run migrations
    print("🔄 Running database migrations...")
    if not run_command(f"{pip_cmd} run python manage.py makemigrations"):
        print("❌ Failed to make migrations")
        return False
    
    if not run_command(f"{pip_cmd} run python manage.py migrate"):
        print("❌ Failed to run migrations")
        return False
    
    # Create superuser
    print("👤 Creating superuser...")
    print("Please enter the following details for the admin user:")
    username = input("Username (default: admin): ") or "admin"
    email = input("Email: ")
    password = input("Password: ")
    
    if not run_command(f"{pip_cmd} run python manage.py createsuperuser --username {username} --email {email} --noinput"):
        print("❌ Failed to create superuser")
        return False
    
    # Set up initial data
    print("📊 Setting up initial data...")
    if not run_command(f"{pip_cmd} run python manage.py setup_initial_data"):
        print("⚠️  Failed to setup initial data (this is optional)")
    
    # Collect static files
    print("📁 Collecting static files...")
    if not run_command(f"{pip_cmd} run python manage.py collectstatic --noinput"):
        print("❌ Failed to collect static files")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Run the development server:")
    print("   python manage.py runserver")
    print("3. Open your browser and go to: http://127.0.0.1:8000/")
    print("4. Admin panel: http://127.0.0.1:8000/admin/")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    
    return True

if __name__ == "__main__":
    setup_local() 