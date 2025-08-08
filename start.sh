#!/bin/bash

# Stable Diffusion API Startup Script

echo "==================================="
echo "Stable Diffusion API Starting..."
echo "==================================="

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container"
    ENVIRONMENT="docker"
else
    echo "Running in local environment"
    ENVIRONMENT="local"
fi

# Check for NVIDIA GPU
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader,nounits
else
    echo "Warning: nvidia-smi not found. Make sure NVIDIA drivers are installed."
fi

# Check CUDA availability
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA devices: {torch.cuda.device_count()}') if torch.cuda.is_available() else None"

# Create output directories
echo "Creating output directories..."
mkdir -p final_outputs upscaled_outputs scheduler_outputs custom_upscaled quality_comparison speed_comparison

# Set environment variables
export PYTHONUNBUFFERED=1

# Start the FastAPI service
echo "Starting FastAPI service on port 8000..."
echo "API will be available at: http://localhost:8000"
echo "Interactive docs at: http://localhost:8000/docs"
echo "==================================="

if [ "$ENVIRONMENT" = "docker" ]; then
    # In Docker, run directly
    exec python3 fastapi_service.py
else
    # In local environment, you might want to activate a virtual environment
    if [ -d "venv" ]; then
        echo "Activating virtual environment..."
        source venv/bin/activate
    fi
    
    python3 fastapi_service.py
fi
