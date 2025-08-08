#!/bin/bash

# Docker Installation Script to Handle Dependency Conflicts
# This script handles pip dependency conflicts during Docker build

set -e

echo "🔧 Installing Python dependencies with conflict resolution..."

# Update pip and core tools first
python3 -m pip install --upgrade pip setuptools wheel

# Install core packages first (these are most likely to have conflicts)
echo "📦 Installing core packages..."
python3 -m pip install --no-deps torch torchvision

# Install packages that commonly conflict, with --force-reinstall if needed
echo "📦 Installing packages with potential conflicts..."
python3 -m pip install --force-reinstall --no-deps \
    numpy>=1.24.0 \
    pillow>=9.0.0 \
    pyyaml>=6.0

# Install main AI/ML packages
echo "📦 Installing AI/ML packages..."
python3 -m pip install \
    diffusers>=0.20.0 \
    transformers>=4.30.0 \
    accelerate \
    safetensors>=0.3.0 \
    huggingface-hub>=0.16.0 \
    tokenizers>=0.13.0

# Install web framework
echo "📦 Installing web framework..."
python3 -m pip install \
    fastapi>=0.100.0 \
    "uvicorn[standard]>=0.20.0" \
    pydantic>=2.0.0 \
    python-multipart>=0.0.5

# Install Streamlit (may have dependency conflicts)
echo "📦 Installing Streamlit..."
python3 -m pip install streamlit>=1.25.0

# Install image processing
echo "📦 Installing image processing packages..."
python3 -m pip install \
    opencv-python>=4.7.0 \
    scikit-image>=0.20.0 \
    imageio>=2.25.0 \
    scipy>=1.10.0 \
    matplotlib>=3.6.0

# Install upscaling packages (these often have conflicts)
echo "📦 Installing upscaling packages..."
python3 -m pip install \
    realesrgan || echo "⚠️  realesrgan installation failed, continuing..."

python3 -m pip install \
    basicsr || echo "⚠️  basicsr installation failed, continuing..."

python3 -m pip install \
    gfpgan || echo "⚠️  gfpgan installation failed, continuing..."

# Install remaining utilities
echo "📦 Installing utilities..."
python3 -m pip install \
    requests>=2.28.0 \
    tqdm>=4.60.0 \
    packaging>=21.0 \
    filelock>=3.8.0

echo "✅ Python dependencies installation completed!"
echo "📝 Some packages may have been skipped due to conflicts, but core functionality should work."
