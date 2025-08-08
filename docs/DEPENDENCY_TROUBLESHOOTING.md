# 🔧 Dependency Installation Troubleshooting Guide

## 🚨 Common Dependency Errors and Solutions

### Error: "Cannot uninstall blinker 1.4 - distutils installed project"

**Cause**: System packages installed via distutils cannot be safely uninstalled by pip.

**Solutions**:

#### Option 1: Use Virtual Environment (Recommended)
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Then install requirements
pip install -r requirements.txt
```

#### Option 2: Force Installation (Docker)
```bash
# Use our conflict resolution script
./fix_dependencies.sh
```

#### Option 3: Skip Conflicting Packages
```bash
# Install core packages only
pip install -r requirements_minimal.txt
```

### Error: "Building wheel for basicsr/filterpy failed"

**Cause**: Legacy packages using old build systems.

**Solutions**:

#### Option 1: Install without these packages
```bash
# Remove these lines from requirements.txt temporarily:
# basicsr
# gfpgan  
# realesrgan

pip install -r requirements.txt

# Then install manually:
pip install basicsr --no-build-isolation
pip install gfpgan --no-build-isolation
pip install realesrgan --no-build-isolation
```

#### Option 2: Use our automated script
```bash
./install_dependencies.sh
```

### Error: "NVIDIA CUDA package conflicts"

**Cause**: Multiple CUDA package versions conflicting.

**Solutions**:

#### Let PyTorch manage CUDA dependencies:
```bash
# Uninstall all nvidia packages
pip uninstall nvidia-* -y

# Install PyTorch (it will handle CUDA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Then install other packages
pip install diffusers transformers fastapi streamlit
```

### Error: "Package version conflicts"

**Cause**: Pinned package versions that conflict with system packages.

**Solutions**:

#### Use version ranges instead of exact pins:
```bash
# Instead of: package==1.2.3
# Use:        package>=1.2.0
```

#### Or use our clean requirements:
```bash
pip install -r requirements_clean.txt
```

## 🐳 Docker-Specific Issues

### Error: "Docker build fails during pip install"

**Solutions**:

#### Option 1: Use multi-stage build
```dockerfile
# Add to Dockerfile before pip install:
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
```

#### Option 2: Use our installation script
The Dockerfile already includes our conflict resolution script.

#### Option 3: Build without cache
```bash
docker build --no-cache -t stable-diffusion-studio .
```

### Error: "Container exits with dependency errors"

**Solutions**:

#### Debug the container:
```bash
# Run container in interactive mode
docker run -it --gpus all stable-diffusion-studio /bin/bash

# Then manually run installation scripts
./fix_dependencies.sh
```

## 🎯 Quick Fixes by Use Case

### "I just want to run the app locally"
```bash
# Use minimal requirements
pip install torch diffusers transformers fastapi streamlit
python3 fastapi_service.py
```

### "I want full functionality"
```bash
# Use our fix script
./fix_dependencies.sh
```

### "I'm developing/testing"
```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "I'm deploying to production"
```bash
# Use Docker with our conflict resolution
docker build -t stable-diffusion-studio .
docker run --gpus all -p 8000:8000 -p 8501:8501 stable-diffusion-studio
```

## 🔍 Diagnostic Commands

### Check your Python environment:
```bash
python3 --version
pip --version
pip list | grep -E "(torch|diffusers|fastapi|streamlit)"
```

### Check for conflicting packages:
```bash
pip check
```

### Check CUDA availability:
```bash
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Test core imports:
```bash
python3 -c "
import torch
import diffusers  
import transformers
import fastapi
import streamlit
print('All imports successful!')
"
```

## 📝 Alternative Installation Methods

### Method 1: Conda Environment
```bash
conda create -n stablediffusion python=3.12
conda activate stablediffusion
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
pip install diffusers transformers fastapi streamlit
```

### Method 2: System Package Manager
```bash
# Ubuntu/Debian
sudo apt install python3-torch python3-pip
pip install diffusers transformers fastapi streamlit

# macOS with Homebrew  
brew install python
pip3 install torch diffusers transformers fastapi streamlit
```

### Method 3: Pre-built Docker Images
```bash
# Use official PyTorch image as base
docker run --gpus all -it pytorch/pytorch:latest bash
# Then install our requirements
```

## 🆘 Still Having Issues?

1. **Check the logs**: Look for specific error messages
2. **Use minimal requirements**: Start with `requirements_minimal.txt`
3. **Try our fix script**: `./fix_dependencies.sh`
4. **Use virtual environment**: Isolate from system packages
5. **Check Python version**: We recommend Python 3.10-3.12
6. **Update pip**: `pip install --upgrade pip setuptools wheel`

## 📞 Getting Help

If you're still having issues:

1. **Check the error message** for specific package names
2. **Run our diagnostic commands** above
3. **Try the appropriate quick fix** for your use case
4. **Use the backup requirements** if needed: `requirements_original_backup.txt`

**Remember**: The core functionality (image generation) works with just:
```bash
pip install torch diffusers transformers fastapi streamlit
```

Everything else is optional enhancement!
