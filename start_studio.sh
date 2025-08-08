#!/bin/bash

# Multi-Service Startup Script
# Starts both FastAPI backend and Streamlit frontend

set -e

echo "🚀 Starting Stable Diffusion Studio"
echo "==================================="

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        
        echo "   Attempt $attempt/$max_attempts - waiting..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ $service_name failed to start within timeout"
    return 1
}

# Start FastAPI backend
echo "🔧 Starting FastAPI backend..."
if check_port 8000; then
    echo "✅ FastAPI already running on port 8000"
else
    echo "🚀 Launching FastAPI service..."
    python3 fastapi_service.py &
    FASTAPI_PID=$!
    echo "FastAPI PID: $FASTAPI_PID"
    
    # Wait for FastAPI to be ready
    if ! wait_for_service "http://localhost:8000/health" "FastAPI"; then
        echo "❌ Failed to start FastAPI backend"
        kill $FASTAPI_PID 2>/dev/null || true
        exit 1
    fi
fi

# Start Streamlit frontend
echo "🎨 Starting Streamlit frontend..."
if check_port 8501; then
    echo "✅ Streamlit already running on port 8501"
else
    echo "🚀 Launching Streamlit UI..."
    streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true &
    STREAMLIT_PID=$!
    echo "Streamlit PID: $STREAMLIT_PID"
    
    # Wait for Streamlit to be ready
    if ! wait_for_service "http://localhost:8501" "Streamlit"; then
        echo "❌ Failed to start Streamlit frontend"
        kill $STREAMLIT_PID 2>/dev/null || true
        kill $FASTAPI_PID 2>/dev/null || true
        exit 1
    fi
fi

echo ""
echo "🎉 Stable Diffusion Studio is ready!"
echo "==================================="
echo "📡 FastAPI Backend:  http://localhost:8000"
echo "🌐 Swagger UI:       http://localhost:8000/docs"
echo "🎨 Streamlit UI:     http://localhost:8501"
echo ""
echo "💡 Use the Streamlit interface for the best user experience!"
echo ""

# Keep script running and handle cleanup
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill $STREAMLIT_PID 2>/dev/null || true
        echo "✅ Streamlit stopped"
    fi
    if [ ! -z "$FASTAPI_PID" ]; then
        kill $FASTAPI_PID 2>/dev/null || true
        echo "✅ FastAPI stopped"
    fi
    echo "👋 Goodbye!"
    exit 0
}

# Trap signals for cleanup
trap cleanup SIGINT SIGTERM

# Wait for user input or signals
echo "Press Ctrl+C to stop both services..."
wait
