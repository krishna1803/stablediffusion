#!/bin/bash

# Dependency Conflict Resolution Script
# Run this if you encounter pip dependency conflicts

set -e

echo "🔧 Resolving Python dependency conflicts..."
echo "========================================="

# Function to safely install packages
safe_install() {
    local package=$1
    echo "📦 Installing $package..."
    pip install "$package" 2>/dev/null || {
        echo "⚠️  $package installation failed, trying with --force-reinstall..."
        pip install --force-reinstall --no-deps "$package" 2>/dev/null || {
            echo "❌ $package installation failed completely, skipping..."
        }
    }
}

# Function to handle system package conflicts  
handle_system_conflicts() {
    echo "🛠️  Handling system package conflicts..."
    
    # Remove problematic system packages that conflict
    pip uninstall -y blinker || echo "blinker not found, continuing..."
    pip uninstall -y setuptools || echo "setuptools not found, continuing..."
    
    # Reinstall with compatible versions
    pip install --upgrade setuptools wheel pip
}

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Not in a virtual environment!"
    echo "   It's recommended to use a virtual environment to avoid system conflicts."
    read -p "   Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Aborted. Please activate a virtual environment first:"
        echo "   python3 -m venv venv"
        echo "   source venv/bin/activate"
        exit 1
    fi
fi

# Step 1: Handle system conflicts
handle_system_conflicts

# Step 2: Install core packages first
echo "📦 Installing core packages..."
safe_install "torch>=2.0.0"
safe_install "torchvision>=0.15.0"
safe_install "numpy"
safe_install "pillow"

# Step 3: Install main AI packages
echo "📦 Installing AI/ML packages..."
safe_install "diffusers>=0.20.0"
safe_install "transformers>=4.30.0"
safe_install "accelerate"
safe_install "safetensors"

# Step 4: Install web framework
echo "📦 Installing web framework..."
safe_install "fastapi"
safe_install "uvicorn[standard]"
safe_install "pydantic"
safe_install "python-multipart"

# Step 5: Install Streamlit
echo "📦 Installing Streamlit..."
safe_install "streamlit"

# Step 6: Install remaining packages
echo "📦 Installing remaining packages..."
safe_install "requests"
safe_install "opencv-python"
safe_install "scikit-image"
safe_install "imageio"
safe_install "scipy"
safe_install "matplotlib"
safe_install "tqdm"
safe_install "pyyaml"
safe_install "huggingface-hub"
safe_install "tokenizers"

# Step 7: Try to install upscaling packages (optional)
echo "📦 Installing upscaling packages (optional)..."
echo "   These may fail due to dependencies, but core functionality will work."

safe_install "realesrgan"
safe_install "basicsr"
safe_install "gfpgan"

echo ""
echo "✅ Dependency installation completed!"
echo "🧪 Testing imports..."

# Test critical imports
python3 -c "
import torch
import diffusers
import transformers
import fastapi
import streamlit
print('✅ All critical packages imported successfully!')
" || echo "❌ Some imports failed, but you may still be able to run the application."

echo ""
echo "🎉 Setup complete! You can now run:"
echo "   ./run_local.sh    # For local development"
echo "   ./deploy.sh       # For Docker deployment"
