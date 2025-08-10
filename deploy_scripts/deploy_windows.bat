@echo off
echo 🚀 Hospital Management System - Windows Deployment Script
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python first.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed. Please install Git first.
    echo Visit: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo ✅ Python and Git are installed
echo.

REM Initialize Git repository if not already done
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit: Hospital Management System"
    echo ✅ Git repository initialized
    echo.
)

REM Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput
echo ✅ Static files collected
echo.

REM Run migrations
echo 🔄 Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo ✅ Migrations completed
echo.

echo 🎯 Next Steps:
echo 1. Create a GitHub repository at https://github.com
echo 2. Push your code to GitHub:
echo    git remote add origin https://github.com/YOUR_USERNAME/hospital-management-system.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Choose your deployment platform:
echo    - Heroku: https://devcenter.heroku.com/articles/getting-started-with-python
echo    - Railway: https://railway.app
echo    - Render: https://render.com
echo.
echo 4. Follow the deployment guide in DEPLOYMENT_GUIDE.md
echo.

pause 