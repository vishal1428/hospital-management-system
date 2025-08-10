# Hospital Management System

A comprehensive Django-based Hospital Management System that provides a complete solution for managing hospital operations, appointments, doctor-patient interactions, and administrative tasks.

## 🏥 Features

### For Patients
- User registration and authentication
- Book appointments with doctors
- View appointment history and status
- Profile management
- Payment processing
- Real-time notifications

### For Doctors
- Professional profile management
- Appointment scheduling and management
- Patient history access
- Payment tracking
- Dashboard with analytics

### For Administrators
- Complete hospital management
- Doctor and patient management
- Service and department management
- Appointment oversight
- System analytics

## 🛠️ Technologies Used

- **Backend**: Django 4.2.2
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (Development), PostgreSQL (Production)
- **Authentication**: Django's built-in authentication system
- **Payment**: Integrated payment processing
- **Email**: Django Anymail for email notifications
- **UI Framework**: Django Jazzmin for admin interface

## 📋 Prerequisites

- Python 3.8+
- pip
- Git

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hospital-management-system.git
   cd hospital-management-system
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
Hospital_Management/
├── base/                 # Core application
├── doctor/              # Doctor-specific functionality
├── patient/             # Patient-specific functionality
├── userauths/           # Authentication system
├── HMS_prj/             # Project settings
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User-uploaded files
└── requirements.txt     # Python dependencies
```

## 🔧 Configuration

### Database Configuration
The system uses SQLite by default for development. For production, configure PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Email Configuration
Configure email settings in settings.py for appointment notifications:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 🚀 Deployment

### Deploy to Heroku

1. **Install Heroku CLI**
2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Add PostgreSQL addon**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Configure environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Run migrations**
   ```bash
   heroku run python manage.py migrate
   ```

### Deploy to Railway

1. **Connect your GitHub repository to Railway**
2. **Set environment variables in Railway dashboard**
3. **Deploy automatically on push**

## 📱 Usage

### For Patients
1. Register an account
2. Browse available doctors and services
3. Book appointments
4. Make payments
5. Track appointment status

### For Doctors
1. Create professional profile
2. Set availability
3. Manage appointments
4. View patient information
5. Track earnings

### For Administrators
1. Access admin panel
2. Manage users, doctors, and services
3. Monitor system activity
4. Generate reports

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive UI components
- All contributors who helped improve this project

## 📞 Support

If you have any questions or need support, please open an issue on GitHub or contact us at your-email@example.com.

## 🔄 Version History

- **v1.0.0** - Initial release with basic functionality
- **v1.1.0** - Added payment processing
- **v1.2.0** - Enhanced UI and user experience
- **v1.3.0** - Added real-time notifications

---

**Note**: This is a demonstration project. For production use, ensure proper security measures, data backup, and compliance with healthcare regulations. 