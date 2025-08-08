#!/bin/bash

# Local Development Launcher for Stable Diffusion Studio
# This script starts both FastAPI and Streamlit locally (without Docker)

set -e

echo "🚀 Starting Stable Diffusion Studio (Local Development)"
echo "======================================================"

# Check for virtual environment and activate if available
if [ -d "venv" ]; then
    echo "🐍 Activating local virtual environment..."
    source venv/bin/activate
    echo "✅ Local virtual environment activated: $(which python)"
elif [ -d "/opt/venv" ]; then
    echo "🐍 Activating container virtual environment..."
    source /opt/venv/bin/activate
    export PATH="/opt/venv/bin:$PATH"
    echo "✅ Container virtual environment activated: $(which python)"
elif [ -n "$VIRTUAL_ENV" ]; then
    echo "🐍 Using existing virtual environment: $VIRTUAL_ENV"
else
    echo "ℹ️  No virtual environment detected, using system Python"
fi

# Check if Python dependencies are installed
check_dependencies() {
    echo "🔍 Checking dependencies..."
    
    # Check if required packages are installed
    python3 -c "import fastapi, uvicorn, streamlit, requests, PIL" 2>/dev/null || {
        echo "❌ Missing dependencies. Installing..."
        if [ -n "$VIRTUAL_ENV" ]; then
            pip install -r config/requirements.txt
        else
            pip3 install -r config/requirements.txt
        fi
    }
    
    echo "✅ Dependencies OK"
}

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to wait for service
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=15
    local attempt=1
    
    echo "⏳ Waiting for $service_name..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        
        echo "   Attempt $attempt/$max_attempts"
        sleep 1
        attempt=$((attempt + 1))
    done
    
    echo "❌ $service_name failed to start"
    return 1
}

# Check dependencies first
check_dependencies

echo ""
echo "🔧 Starting FastAPI backend..."
if check_port 8000; then
    echo "✅ FastAPI already running on port 8000"
else
    python3 fastapi_service.py &
    FASTAPI_PID=$!
    echo "FastAPI PID: $FASTAPI_PID"
    
    if ! wait_for_service "http://localhost:8000/health" "FastAPI"; then
        echo "❌ Failed to start FastAPI"
        kill $FASTAPI_PID 2>/dev/null || true
        exit 1
    fi
fi

echo ""
echo "🎨 Starting Streamlit frontend..."
if check_port 8501; then
    echo "✅ Streamlit already running on port 8501"
else
    streamlit run streamlit_app.py --server.port 8501 --server.address localhost &
    STREAMLIT_PID=$!
    echo "Streamlit PID: $STREAMLIT_PID"
    
    if ! wait_for_service "http://localhost:8501" "Streamlit"; then
        echo "❌ Failed to start Streamlit"
        kill $STREAMLIT_PID 2>/dev/null || true
        if [ ! -z "$FASTAPI_PID" ]; then
            kill $FASTAPI_PID 2>/dev/null || true
        fi
        exit 1
    fi
fi

echo ""
echo "🎉 Stable Diffusion Studio is ready!"
echo "======================================"
echo "🌐 Streamlit UI:     http://localhost:8501"
echo "📡 FastAPI Backend:  http://localhost:8000"
echo "📚 API Docs:         http://localhost:8000/docs"
echo ""
echo "💡 Open http://localhost:8501 in your browser!"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill $STREAMLIT_PID 2>/dev/null || true
        echo "✅ Streamlit stopped"
    fi
    if [ ! -z "$FASTAPI_PID" ]; then
        kill $FASTAPI_PID 2>/dev/null || true
        echo "✅ FastAPI stopped"
    fi
    exit 0
}

# Trap signals
trap cleanup SIGINT SIGTERM

echo "Press Ctrl+C to stop..."
wait
