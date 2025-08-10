#!/bin/bash
# Build script for Railway deployment

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🔄 Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Set up initial data
echo "📊 Setting up initial data..."
python manage.py setup_initial_data

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!" 