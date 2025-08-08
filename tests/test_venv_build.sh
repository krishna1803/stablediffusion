#!/bin/bash

# Test Virtual Environment Docker Build
# This script tests if the virtual environment approach resolves dependency conflicts

set -e

echo "🧪 Testing Virtual Environment Docker Build"
echo "==========================================="

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

echo "🔧 Building Docker image with virtual environment approach..."

# Build the image
if docker build -t stable-diffusion-studio-test . ; then
    echo "✅ Docker build successful!"
    
    echo "🧪 Testing virtual environment in container..."
    
    # Test virtual environment setup
    echo "📋 Virtual Environment Details:"
    docker run --rm stable-diffusion-studio-test bash -c "
        echo 'Virtual Environment: \$VIRTUAL_ENV'
        echo 'Python Path: \$PATH'
        echo 'Python executable: \$(which python)'
        echo 'Python version: \$(python --version)'
        echo 'Pip location: \$(which pip)'
        echo 'Checking if venv is active...'
        if [ -n '\$VIRTUAL_ENV' ]; then
            echo '✅ Virtual environment is active'
        else
            echo '❌ Virtual environment not active'
        fi
    "
    
    echo ""
    echo "📦 Testing key packages:"
    docker run --rm stable-diffusion-studio-test python -c "
import sys
print('Python executable:', sys.executable)
print('Python path:', sys.path[0])

# Test key imports
try:
    import torch
    print('✅ PyTorch:', torch.__version__)
except ImportError as e:
    print('❌ PyTorch import failed:', e)

try:
    import fastapi
    print('✅ FastAPI:', fastapi.__version__)
except ImportError as e:
    print('❌ FastAPI import failed:', e)
    
try:
    import streamlit
    print('✅ Streamlit:', streamlit.__version__)
except ImportError as e:
    print('❌ Streamlit import failed:', e)
    
try:
    import diffusers
    print('✅ Diffusers:', diffusers.__version__)
except ImportError as e:
    print('❌ Diffusers import failed:', e)
"
    
    # Test if virtual environment is active
    docker run --rm stable-diffusion-studio-test bash -c 'echo "Virtual env: $VIRTUAL_ENV"'
    
    # Test key package imports
    docker run --rm stable-diffusion-studio-test python -c "
import sys
print(f'Python: {sys.version}')
print(f'Executable: {sys.executable}')
try:
    import torch
    print('✅ PyTorch imported successfully')
except ImportError as e:
    print(f'❌ PyTorch import failed: {e}')
    
try:
    import diffusers
    print('✅ Diffusers imported successfully')  
except ImportError as e:
    print(f'❌ Diffusers import failed: {e}')
    
try:
    import fastapi
    print('✅ FastAPI imported successfully')
except ImportError as e:
    print(f'❌ FastAPI import failed: {e}')
    
try:
    import streamlit
    print('✅ Streamlit imported successfully')
except ImportError as e:
    print(f'❌ Streamlit import failed: {e}')
"
    
    echo ""
    echo "🎉 Virtual environment test completed!"
    echo "📋 Build log saved to: docker_build.log"
    
else
    echo "❌ Docker build failed!"
    echo "📋 Check docker_build.log for details"
    echo ""
    echo "🔍 Last 20 lines of build log:"
    tail -20 docker_build.log
    exit 1
fi
