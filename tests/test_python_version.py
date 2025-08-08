#!/usr/bin/env python3
"""
Python Version Test Script

This script tests that Python 3.12 is properly installed and configured.
Run this inside the Docker container to verify the setup.
"""

import sys
import platform
import subprocess
import os

def test_python_version():
    """Test Python version and configuration."""
    print("🐍 Python Version Test")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        print(f"🌐 Virtual Environment: {venv_path}")
    else:
        print("🌐 Virtual Environment: Not detected")
    
    # Check Python version
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    print(f"Full Version Info: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    
    # Check if we're running Python 3.12
    if version.major == 3 and version.minor == 12:
        print("✅ Python 3.12 is correctly installed and running!")
    else:
        print(f"❌ Expected Python 3.12, but got {version.major}.{version.minor}")
        return False
    
    # Check Python executable paths
    print(f"\nPython Executable: {sys.executable}")
    
    # Test import of key packages
    print("\n📦 Testing Key Package Imports...")
    test_packages = [
        'torch',
        'diffusers', 
        'fastapi',
        'uvicorn',
        'PIL',
        'requests',
        'streamlit'
    ]
    
    for package in test_packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {package}: {e}")
            return False
    
    # Test pip version
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        print(f"\nPip Version: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Error checking pip version: {e}")
    
    # Test PyTorch CUDA availability
    try:
        import torch
        print(f"\n🔥 PyTorch CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"🔥 CUDA Device Count: {torch.cuda.device_count()}")
            print(f"🔥 CUDA Device Name: {torch.cuda.get_device_name(0)}")
    except:
        print("⚠️  Could not check CUDA availability")
    
    print("\n🎉 All Python 3.12 tests passed!")
    return True

if __name__ == "__main__":
    success = test_python_version()
    sys.exit(0 if success else 1)
