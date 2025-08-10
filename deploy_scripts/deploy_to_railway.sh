#!/bin/bash

# Hospital Management System - Railway Deployment Script

echo "🚀 Starting Railway deployment..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed. Please install it first."
    echo "Visit: https://docs.railway.app/develop/cli"
    exit 1
fi

# Check if user is logged in to Railway
if ! railway whoami &> /dev/null; then
    echo "❌ Please login to Railway first:"
    railway login
fi

# Initialize Railway project if not already done
if [ ! -f "railway.json" ]; then
    echo "📦 Initializing Railway project..."
    railway init
fi

# Deploy to Railway
echo "📤 Deploying to Railway..."
railway up

echo "✅ Deployment completed!"
echo "🌐 Your app is live at the URL shown above"
echo "🔧 You can manage your deployment at: https://railway.app/dashboard" 