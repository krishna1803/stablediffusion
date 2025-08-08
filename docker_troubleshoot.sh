#!/bin/bash

# Docker Build Troubleshooting Script
# This script helps diagnose and fix Docker build issues

set -e

echo "🔧 Docker Build Troubleshooting Script"
echo "======================================="

# Function to check Docker installation
check_docker() {
    echo "🐳 Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed!"
        echo "Please install Docker first: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    echo "✅ Docker is installed: $(docker --version)"
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        echo "❌ Docker daemon is not running!"
        echo "Please start Docker daemon and try again."
        exit 1
    fi
    
    echo "✅ Docker daemon is running"
}

# Function to check internet connectivity
check_connectivity() {
    echo "🌐 Checking internet connectivity..."
    
    if ! ping -c 1 google.com &> /dev/null; then
        echo "❌ No internet connection!"
        echo "Please check your internet connection and try again."
        exit 1
    fi
    
    echo "✅ Internet connection is working"
    
    # Check Docker Hub connectivity
    if ! docker pull hello-world &> /dev/null; then
        echo "⚠️  Warning: Cannot pull from Docker Hub"
        echo "This might cause issues with NVIDIA CUDA images"
    else
        echo "✅ Docker Hub is accessible"
        docker rmi hello-world &> /dev/null
    fi
}

# Function to check available CUDA images
check_cuda_images() {
    echo "🎯 Checking NVIDIA CUDA image availability..."
    
    # List of CUDA images to try (in order of preference)
    CUDA_IMAGES=(
        "nvidia/cuda:12.2-runtime-ubuntu22.04"
        "nvidia/cuda:12.1-devel-ubuntu22.04"
        "nvidia/cuda:12.1-runtime-ubuntu22.04"
        "nvidia/cuda:11.8-runtime-ubuntu22.04"
        "nvidia/cuda:11.8-devel-ubuntu22.04"
        "nvidia/cuda:latest"
    )
    
    WORKING_IMAGE=""
    
    for image in "${CUDA_IMAGES[@]}"; do
        echo "  Testing: $image"
        if docker pull "$image" &> /dev/null; then
            echo "  ✅ $image is available"
            WORKING_IMAGE="$image"
            break
        else
            echo "  ❌ $image is not available"
        fi
    done
    
    if [ -z "$WORKING_IMAGE" ]; then
        echo "❌ No NVIDIA CUDA images are available!"
        echo "Falling back to Ubuntu base image..."
        WORKING_IMAGE="ubuntu:22.04"
    fi
    
    echo "🎯 Recommended image: $WORKING_IMAGE"
}

# Function to update Dockerfile with working image
update_dockerfile() {
    local working_image="$1"
    echo "📝 Updating Dockerfile with working image: $working_image"
    
    # Backup original Dockerfile
    cp Dockerfile Dockerfile.backup
    
    # Update the FROM line
    sed -i.tmp "s|FROM nvidia/cuda:.*|FROM $working_image|g" Dockerfile
    rm -f Dockerfile.tmp
    
    echo "✅ Dockerfile updated (backup saved as Dockerfile.backup)"
}

# Function to try building with different options
try_build() {
    echo "🔨 Attempting to build Docker image..."
    
    # Build with no cache and verbose output
    if docker build --no-cache --progress=plain -t stable-diffusion-api . 2>&1 | tee build.log; then
        echo "✅ Docker build successful!"
        return 0
    else
        echo "❌ Docker build failed. Check build.log for details."
        return 1
    fi
}

# Function to show alternative solutions
show_alternatives() {
    echo ""
    echo "🔄 Alternative Solutions:"
    echo "========================"
    echo ""
    echo "1. 📋 Use pre-built Dockerfile alternatives:"
    echo "   cp Dockerfile.alternative Dockerfile"
    echo "   docker build -t stable-diffusion-api ."
    echo ""
    echo "2. 🌐 Try building with different networks:"
    echo "   docker build --network=host -t stable-diffusion-api ."
    echo ""
    echo "3. 🏗️  Build without cache:"
    echo "   docker build --no-cache -t stable-diffusion-api ."
    echo ""
    echo "4. 🔧 Use Docker buildx for multi-platform builds:"
    echo "   docker buildx build --platform linux/amd64 -t stable-diffusion-api ."
    echo ""
    echo "5. 📦 Build with specific Docker context:"
    echo "   docker build --build-arg BUILDKIT_INLINE_CACHE=1 -t stable-diffusion-api ."
    echo ""
    echo "6. 🐧 Use Ubuntu base image (if NVIDIA images fail):"
    echo "   # Edit Dockerfile and change FROM line to:"
    echo "   # FROM ubuntu:22.04"
    echo ""
    echo "7. 🔗 Check proxy/firewall settings:"
    echo "   # If behind corporate firewall, configure Docker proxy"
    echo "   # See: https://docs.docker.com/network/proxy/"
}

# Main execution
main() {
    check_docker
    check_connectivity
    check_cuda_images
    
    echo ""
    echo "🎯 Attempting Docker build with best available image..."
    
    if [ "$WORKING_IMAGE" != "nvidia/cuda:12.1-devel-ubuntu22.04" ]; then
        read -p "Update Dockerfile with working image ($WORKING_IMAGE)? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            update_dockerfile "$WORKING_IMAGE"
        fi
    fi
    
    if try_build; then
        echo ""
        echo "🎉 SUCCESS! Docker image built successfully!"
        echo "You can now run: docker run --gpus all -p 8000:8000 stable-diffusion-api"
    else
        echo ""
        echo "❌ Build failed. Here are some alternatives:"
        show_alternatives
        
        echo ""
        echo "📋 Common Error Solutions:"
        echo "========================="
        echo "• Image not found: Try different CUDA version"
        echo "• Network timeout: Check internet/proxy settings"
        echo "• Permission denied: Run with sudo or check Docker permissions"
        echo "• Disk space: Clean up Docker images (docker system prune)"
        echo "• Memory issues: Increase Docker memory limits"
        
        exit 1
    fi
}

# Run main function
main "$@"
