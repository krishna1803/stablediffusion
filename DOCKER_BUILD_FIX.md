# 🐳 Docker Build Fix Guide

## The Error You're Seeing

```bash
ERROR [internal] load metadata for docker.io/nvidia/cuda:12.1-runtime-ubuntu22.04
```

This error occurs when:
1. The specific CUDA image version is not available
2. Network connectivity issues
3. Docker Hub access problems
4. Regional/proxy restrictions

## ✅ Solutions (Try in Order)

### Solution 1: Updated Dockerfile (Recommended)

I've updated your Dockerfile with a more reliable image. Use the current `Dockerfile` which now uses:
```dockerfile
FROM nvidia/cuda:12.1-devel-ubuntu22.04
```

### Solution 2: Alternative CUDA Images

If the main image still fails, edit your `Dockerfile` and try these alternatives:

```dockerfile
# Option A: Latest stable CUDA runtime
FROM nvidia/cuda:12.2-runtime-ubuntu22.04

# Option B: CUDA 11.8 (widely available)
FROM nvidia/cuda:11.8-runtime-ubuntu22.04

# Option C: Latest CUDA
FROM nvidia/cuda:latest

# Option D: Ubuntu with manual CUDA (fallback)
FROM ubuntu:22.04
```

### Solution 3: Automated Troubleshooting

Run the troubleshooting script I've created:

```bash
./docker_troubleshoot.sh
```

This will:
- ✅ Check Docker installation
- ✅ Test internet connectivity  
- ✅ Find working CUDA images
- ✅ Automatically update Dockerfile
- ✅ Attempt build with best options

### Solution 4: Manual Build Commands

Try these build commands in order:

```bash
# 1. Build with no cache
docker build --no-cache -t stable-diffusion-api .

# 2. Build with host network
docker build --network=host -t stable-diffusion-api .

# 3. Build with verbose output
docker build --progress=plain -t stable-diffusion-api .

# 4. Build with specific platform
docker buildx build --platform linux/amd64 -t stable-diffusion-api .
```

### Solution 5: Use Alternative Dockerfile

```bash
# Use the alternative Dockerfile with multiple options
cp Dockerfile.alternative Dockerfile
docker build -t stable-diffusion-api .
```

## 🖥️ For GPU Servers

If you're building on a GPU server, ensure:

1. **NVIDIA Container Toolkit is installed:**
   ```bash
   # Check if installed
   docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu22.04 nvidia-smi
   
   # If not installed:
   sudo apt-get update
   sudo apt-get install -y nvidia-docker2
   sudo systemctl restart docker
   ```

2. **Docker has GPU access:**
   ```bash
   # Test GPU access
   docker run --rm --gpus all ubuntu:22.04 nvidia-smi
   ```

## 🌐 Network/Proxy Issues

If behind corporate firewall or proxy:

1. **Configure Docker proxy:**
   ```bash
   # Create or edit ~/.docker/config.json
   {
     "proxies": {
       "default": {
         "httpProxy": "http://proxy.company.com:8080",
         "httpsProxy": "http://proxy.company.com:8080"
       }
     }
   }
   ```

2. **Use alternative registries:**
   ```bash
   # Try different registries
   docker pull nvcr.io/nvidia/cuda:12.1-runtime-ubuntu22.04
   ```

## 🔧 Quick Fix Commands

### Check Docker Status
```bash
docker info
docker version
```

### Clean Docker Cache
```bash
docker system prune -a
docker builder prune -a
```

### Check Available Images
```bash
# Search for CUDA images
docker search nvidia/cuda
```

### Test Simple Build
```bash
# Test with simple Ubuntu image first
echo "FROM ubuntu:22.04" > Dockerfile.test
echo "RUN apt-get update" >> Dockerfile.test
docker build -f Dockerfile.test -t test-build .
```

## 📋 Recommended Dockerfile for Maximum Compatibility

Here's a Dockerfile that works in most environments:

```dockerfile
FROM nvidia/cuda:11.8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

RUN apt-get update && apt-get install -y \
    python3 python3-pip curl git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p final_outputs upscaled_outputs scheduler_outputs

EXPOSE 8000
CMD ["python3", "fastapi_service.py"]
```

## 🚀 Deployment Steps

1. **Try the troubleshooting script:**
   ```bash
   ./docker_troubleshoot.sh
   ```

2. **If that fails, manual fix:**
   ```bash
   # Edit Dockerfile - change first line to:
   # FROM nvidia/cuda:11.8-runtime-ubuntu22.04
   
   docker build -t stable-diffusion-api .
   ```

3. **Test the image:**
   ```bash
   docker run --gpus all -p 8000:8000 stable-diffusion-api
   ```

## 🆘 Still Having Issues?

If none of the above work:

1. **Check your specific environment:**
   - OS version
   - Docker version
   - Network restrictions
   - Available disk space

2. **Use Ubuntu base and install CUDA manually:**
   ```dockerfile
   FROM ubuntu:22.04
   # Add manual CUDA installation steps
   ```

3. **Contact support with:**
   - Full error message
   - Docker version (`docker version`)
   - OS information
   - Network environment details

The updated Dockerfile should resolve the issue in most cases! 🎉
