#!/bin/bash

# Hospital Management System - Heroku Deployment Script

echo "🚀 Starting Heroku deployment..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first."
    echo "Visit: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "❌ Please login to Heroku first:"
    heroku login
fi

# Get app name from user
read -p "Enter your Heroku app name: " APP_NAME

# Create Heroku app if it doesn't exist
if ! heroku apps:info --app $APP_NAME &> /dev/null; then
    echo "📦 Creating new Heroku app: $APP_NAME"
    heroku create $APP_NAME
else
    echo "✅ App $APP_NAME already exists"
fi

# Add PostgreSQL addon
echo "🗄️ Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:hobby-dev --app $APP_NAME

# Set environment variables
echo "🔧 Setting environment variables..."
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())') --app $APP_NAME
heroku config:set DEBUG=False --app $APP_NAME
heroku config:set ALLOWED_HOSTS=$APP_NAME.herokuapp.com --app $APP_NAME

# Deploy to Heroku
echo "📤 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku - $(date)"
git push heroku main

# Run migrations
echo "🔄 Running database migrations..."
heroku run python manage.py migrate --app $APP_NAME

# Create superuser if needed
read -p "Do you want to create a superuser? (y/n): " CREATE_SUPERUSER
if [ "$CREATE_SUPERUSER" = "y" ]; then
    heroku run python manage.py createsuperuser --app $APP_NAME
fi

echo "✅ Deployment completed!"
echo "🌐 Your app is live at: https://$APP_NAME.herokuapp.com"
echo "🔧 Admin panel: https://$APP_NAME.herokuapp.com/admin/" 