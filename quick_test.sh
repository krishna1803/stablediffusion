#!/bin/bash

# Quick Deploy and Test Script with Swagger UI
# This script deploys the service and opens Swagger UI for testing

set -e

echo "🚀 Quick Deploy with Swagger UI"
echo "================================"

# Check if service is already running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Service is already running!"
else
    echo "🔄 Starting the service..."
    
    # Check if docker-compose is available
    if command -v docker-compose &> /dev/null && [ -f "docker-compose.yml" ]; then
        echo "Using docker-compose..."
        docker-compose up -d
    else
        echo "Using deploy script..."
        ./deploy.sh start
    fi
    
    # Wait for service to be ready
    echo "⏳ Waiting for service to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "✅ Service is ready!"
            break
        fi
        sleep 2
        echo "   Attempt $i/30..."
    done
fi

# Check if service is responsive
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ Service is not responding. Please check the logs:"
    echo "   docker-compose logs"
    echo "   # or"
    echo "   ./deploy.sh logs"
    exit 1
fi

echo ""
echo "🎉 Service is running! Here are your testing options:"
echo ""
echo "📖 Interactive API Documentation:"
echo "   Swagger UI: http://localhost:8000/docs"
echo "   ReDoc:      http://localhost:8000/redoc"
echo ""
echo "🧪 Testing Tools:"
echo "   Interactive Helper: python3 swagger_tester.py"
echo "   Automated Tests:    python3 test_api.py"
echo "   Usage Examples:     python3 example_usage.py"
echo ""
echo "🔗 Quick Links:"
echo "   Health Check:       http://localhost:8000/health"
echo "   Available Files:    http://localhost:8000/files"
echo "   Available Schedulers: http://localhost:8000/schedulers"
echo ""

# Ask user what they want to do
echo "🎯 What would you like to do?"
echo "1. Open Swagger UI in browser"
echo "2. Run interactive testing helper"
echo "3. Run automated tests"
echo "4. Show service logs"
echo "5. Just show me the URLs"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🌐 Opening Swagger UI..."
        if command -v open &> /dev/null; then
            open http://localhost:8000/docs
        elif command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:8000/docs
        else
            echo "Please manually open: http://localhost:8000/docs"
        fi
        ;;
    2)
        echo "🧪 Starting interactive testing helper..."
        python3 swagger_tester.py
        ;;
    3)
        echo "🔍 Running automated tests..."
        python3 test_api.py
        ;;
    4)
        echo "📋 Service logs:"
        if [ -f "docker-compose.yml" ]; then
            docker-compose logs --tail=50
        else
            ./deploy.sh logs
        fi
        ;;
    5)
        echo "👍 URLs are displayed above. Happy testing!"
        ;;
    *)
        echo "👍 No problem! All URLs are displayed above."
        ;;
esac

echo ""
echo "🎨 Your Stable Diffusion API is ready for testing!"
echo "   Use Swagger UI for the best interactive experience."
