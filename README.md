# Stable Diffusion FastAPI Service

This project provides a comprehensive FastAPI web service for generating images using Stable Diffusion models. The service automatically selects the appropriate model based on available GPU memory and provides multiple upscaling options.

## Features

- **Automatic Model Selection**: Chooses the best Stable Diffusion model based on GPU memory:
  - ≤ 24 GB: Stable Diffusion 2.1
  - 24-48 GB: Stable Diffusion 3.5 Medium
  - \> 48 GB: Stable Diffusion 3.5 Large
- **Multiple Upscaling Methods**: 
  - Single image upscaling (4x)
  - Directory batch upscaling
  - High-resolution upscaling (4x/8x)
- **Scheduler Testing**: Compare 17+ different schedulers
- **RESTful API**: Easy-to-use REST endpoints
- **Docker Support**: Containerized deployment
- **Comprehensive Testing**: Built-in test suite

## Quick Start (Docker - Recommended)

### Prerequisites

- NVIDIA GPU with CUDA support
- Docker with NVIDIA Container Toolkit
- At least 8GB GPU memory (16GB+ recommended)

### One-Command Deployment

```bash
# Full deployment (build, start, test)
./deploy.sh deploy
```

### Manual Docker Steps

```bash
# 1. Build and start with docker-compose
docker-compose up -d

# 2. Or build and run with Docker directly
docker build -t stable-diffusion-api .
docker run --gpus all -p 8000:8000 -v $(pwd)/final_outputs:/app/final_outputs stable-diffusion-api

# 3. Test the deployment
python3 test_api.py
```

## Installation Options

### Option 1: Docker Deployment (Recommended)

1. **Install Prerequisites:**
   - [Docker](https://docs.docker.com/get-docker/)
   - [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

2. **Deploy the Service:**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd stablediffusion
   
   # Deploy with all features
   ./deploy.sh deploy
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs

### Option 2: Local Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Service:**
   ```bash
   python fastapi_service.py
   ```

## API Endpoints

### Image Generation

#### Generate Image
**POST** `/generate`

```json
{
    "prompt": "a beautiful sunset over mountains, digital art",
    "negative_prompt": "blurry, low quality, ugly",
    "num_inference_steps": 50,
    "guidance_scale": 7.0,
    "height": 1024,
    "width": 1024,
    "upscale": false,
    "upscale_prompt": "enhance details"
}
```

### Upscaling

#### Single Image Upscaling
**POST** `/upscale`

```json
{
    "input_file": "image.png",
    "prompt": "enhance details, improve quality",
    "num_inference_steps": 75,
    "guidance_scale": 7.5
}
```

#### Directory Upscaling
**POST** `/upscale-directory`

```json
{
    "input_directory": "path/to/images",
    "prompt": "improve quality",
    "file_extensions": [".png", ".jpg"],
    "num_inference_steps": 50
}
```

#### High-Resolution Upscaling
**POST** `/upscale-highres`

```json
{
    "input_file": "image.png",
    "prompt": "ultra high resolution",
    "use_swinir": true,
    "sd_steps": 75
}
```

### Scheduler Testing

#### Test Multiple Schedulers
**POST** `/test-schedulers`

```json
{
    "prompt": "test image for comparison",
    "schedulers_to_test": ["EulerDiscrete", "DDIM", "DPMSolverMultistep"],
    "num_inference_steps": 30
}
```

#### List Available Schedulers
**GET** `/schedulers`

### Utility

#### Download Generated Image
**GET** `/download/{filename}`

#### Health Check
**GET** `/health`

#### API Documentation
**GET** `/docs` - Interactive Swagger UI

## Deployment Commands

### Using deploy.sh Script

```bash
# Full deployment
./deploy.sh deploy

# Individual commands
./deploy.sh build      # Build Docker image
./deploy.sh start      # Start service
./deploy.sh stop       # Stop service
./deploy.sh restart    # Restart service
./deploy.sh logs       # View logs
./deploy.sh test       # Run tests
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Using Docker Directly

```bash
# Build image
docker build -t stable-diffusion-api .

# Run with GPU support and volume mounts
docker run -d \
  --name stable-diffusion-api \
  --gpus all \
  -p 8000:8000 \
  -v $(pwd)/final_outputs:/app/final_outputs \
  -v $(pwd)/upscaled_outputs:/app/upscaled_outputs \
  stable-diffusion-api

# View logs
docker logs -f stable-diffusion-api

# Stop container
docker stop stable-diffusion-api
```

## Testing

### Automated Testing

```bash
# Test local deployment
python3 test_api.py

# Test remote deployment
python3 test_api.py http://your-server:8000
```

### Manual Testing

```bash
# Health check
curl http://localhost:8000/health

# Generate image
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "a test image", "num_inference_steps": 20}'

# List schedulers
curl http://localhost:8000/schedulers
```

### Interactive Testing

Visit http://localhost:8000/docs for the interactive Swagger UI where you can test all endpoints.

## 🎨 Testing with Swagger UI (Recommended)

Your FastAPI service includes interactive API documentation with Swagger UI - **the easiest way to test your API**!

### Quick Start
```bash
# Deploy and open testing interface
./quick_test.sh

# Or manually:
./deploy.sh deploy
# Then open: http://localhost:8000/docs
```

### Interactive Testing
- **Swagger UI**: http://localhost:8000/docs - Interactive API testing
- **ReDoc**: http://localhost:8000/redoc - Alternative documentation
- **Testing Helper**: `python3 swagger_tester.py` - Menu-driven testing

### Why Use Swagger UI?
✅ **Visual Interface** - No need to write curl commands  
✅ **Live Testing** - Execute API calls directly from the browser  
✅ **Schema Validation** - See parameter types and constraints  
✅ **Real-time Responses** - View results immediately  
✅ **File Downloads** - Download generated images directly  
✅ **Copy Curl Commands** - Get curl equivalents for your code  

See [SWAGGER_UI_GUIDE.md](SWAGGER_UI_GUIDE.md) for detailed usage instructions.

## Configuration

### Environment Variables

```bash
# GPU configuration
NVIDIA_VISIBLE_DEVICES=0    # Specify GPU
CUDA_VISIBLE_DEVICES=0      # CUDA GPU selection

# Python configuration
PYTHONUNBUFFERED=1          # Unbuffered output
```

### Volume Mounts

The Docker setup includes these volume mounts:
- `/app/final_outputs` - Generated images
- `/app/upscaled_outputs` - Upscaled images
- `/app/scheduler_outputs` - Scheduler comparison images

### Model Selection Logic

The service automatically detects GPU memory:

- **≤ 24 GB**: Stable Diffusion 2.1 (`stabilityai/stable-diffusion-2-1`)
- **24-48 GB**: Stable Diffusion 3.5 Medium (`stabilityai/stable-diffusion-3.5-medium`)
- **> 48 GB**: Stable Diffusion 3.5 Large (`stabilityai/stable-diffusion-3.5-large`)

## Troubleshooting

### Common Issues

1. **CUDA/GPU Issues:**
   ```bash
   # Check NVIDIA Docker runtime
   docker info | grep nvidia
   
   # Test GPU access
   docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu22.04 nvidia-smi
   ```

2. **Memory Issues:**
   ```bash
   # Check GPU memory
   nvidia-smi
   
   # Reduce image size or inference steps
   # Use smaller model for lower memory
   ```

3. **Port Conflicts:**
   ```bash
   # Change port in docker-compose.yml or use different port
   docker run -p 8001:8000 stable-diffusion-api
   ```

4. **Permission Issues:**
   ```bash
   # Fix volume permissions
   sudo chown -R $USER:$USER final_outputs upscaled_outputs scheduler_outputs
   ```

### Logs and Debugging

```bash
# View container logs
docker logs stable-diffusion-api

# View docker-compose logs
docker-compose logs -f

# Check container status
docker ps
docker stats stable-diffusion-api
```

## Performance Optimization

### For Better Performance:
- Use SSD storage for model caching
- Increase shared memory: `--shm-size=2g`
- Use multiple GPUs: modify docker-compose.yml
- Optimize inference steps based on quality needs

### For Lower Memory Usage:
- Reduce image dimensions
- Use fewer inference steps
- Enable model offloading in code
- Use float16 precision

## Development

### Local Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run service locally
python fastapi_service.py

# Run individual modules
python imagegeneration_final.py "test prompt" output.png
python image_upscaling.py input.png "enhance details"
python imagegeneration_schedulers.py "test prompt"
```

### Adding New Features

1. Modify the appropriate module (`imagegeneration_final.py`, `image_upscaling.py`, etc.)
2. Update FastAPI endpoints in `fastapi_service.py`
3. Add tests to `test_api.py`
4. Update documentation in `README.md`

## Requirements

- Python 3.8+
- CUDA-capable GPU (8GB+ recommended)
- Docker with NVIDIA Container Toolkit
- See `requirements.txt` for Python dependencies

## Files Structure

```
├── fastapi_service.py              # Main FastAPI service
├── imagegeneration_final.py        # Core image generation
├── image_upscaling.py              # Comprehensive upscaling
├── imagegeneration_schedulers.py   # Scheduler testing
├── deploy.sh                       # Deployment script
├── test_api.py                     # Comprehensive test suite
├── docker-compose.yml              # Docker Compose configuration
├── Dockerfile                      # Docker image definition
├── requirements.txt                # Python dependencies
├── example_usage.py                # Usage examples
├── comprehensive_upscaling_example.py  # Upscaling examples
└── README.md                       # This documentation
```

## License

[Add your license information here]

## Support

For issues and questions:
1. Check the troubleshooting section
2. View logs for error details
3. Test with the provided test suite
4. Create an issue with detailed error information

## Installation

### Option 1: Local Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have CUDA-capable GPU with appropriate drivers installed.

### Option 2: Docker Installation

1. Build the Docker image:
```bash
docker build -t stable-diffusion-api .
```

2. Run with Docker Compose (recommended):
```bash
docker-compose up -d
```

Or run directly with Docker:
```bash
docker run --gpus all -p 8000:8000 -v $(pwd)/final_outputs:/app/final_outputs stable-diffusion-api
```

### Prerequisites

- NVIDIA GPU with CUDA support
- Docker with NVIDIA Container Toolkit (for Docker installation)
- At least 8GB GPU memory (16GB+ recommended)

## Usage

### Starting the FastAPI Server

```bash
python fastapi_service.py
```

The server will start on `http://localhost:8000` by default.

### API Endpoints

#### 1. Generate Image
**POST** `/generate`

Generate an image using Stable Diffusion.

**Request Body:**
```json
{
    "prompt": "a beautiful sunset over mountains, digital art",
    "negative_prompt": "blurry, low quality, ugly, bad anatomy",
    "num_inference_steps": 50,
    "guidance_scale": 7.0,
    "height": 1024,
    "width": 1024,
    "output_dir": "final_outputs"
}
```

**Response:**
```json
{
    "message": "Image generated successfully",
    "output_path": "final_outputs/uuid-filename.png",
    "filename": "uuid-filename.png"
}
```

#### 2. Download Image
**GET** `/download/{filename}`

Download a generated image by filename.

#### 3. Health Check
**GET** `/health`

Check if the service is running.

#### 4. API Documentation
**GET** `/docs`

Interactive API documentation (Swagger UI).

### Command Line Usage

You can still use the script directly from command line:

```bash
python imagegeneration_final.py "a beautiful landscape" "output.png"
```

### Python API Usage

Import and use the functions directly in your Python code:

```python
from imagegeneration_final import generate_image, initialize_pipeline

# Initialize the pipeline (optional - will be done automatically)
initialize_pipeline()

# Generate an image
output_path = generate_image(
    prompt="a beautiful sunset over mountains",
    output_file="sunset.png",
    num_inference_steps=50,
    guidance_scale=7.0
)
print(f"Image saved to: {output_path}")
```

### Using the API with Python Requests

```python
import requests

# Generate an image
response = requests.post("http://localhost:8000/generate", json={
    "prompt": "a futuristic city with flying cars",
    "num_inference_steps": 30,
    "guidance_scale": 7.5
})

if response.status_code == 200:
    result = response.json()
    print(f"Generated: {result['filename']}")
    
    # Download the image
    download_response = requests.get(f"http://localhost:8000/download/{result['filename']}")
    with open(f"downloaded_{result['filename']}", "wb") as f:
        f.write(download_response.content)
```

## Configuration

### Model Selection Logic

The service automatically detects GPU memory and selects the appropriate model:

- **Stable Diffusion 2.1** (≤ 24 GB GPU memory)
  - Model: `stabilityai/stable-diffusion-2-1`
  - Pipeline: `StableDiffusionPipeline`
  - Precision: `float16`

- **Stable Diffusion 3.5 Medium** (24-48 GB GPU memory)
  - Model: `stabilityai/stable-diffusion-3.5-medium`
  - Pipeline: `StableDiffusion3Pipeline`
  - Precision: `bfloat16`

- **Stable Diffusion 3.5 Large** (> 48 GB GPU memory)
  - Model: `stabilityai/stable-diffusion-3.5-large`
  - Pipeline: `StableDiffusion3Pipeline`
  - Precision: `bfloat16`

### Parameters

- **prompt**: Text description of the image to generate
- **negative_prompt**: Text describing what to avoid in the image
- **num_inference_steps**: Number of denoising steps (1-100)
- **guidance_scale**: How closely to follow the prompt (1.0-20.0)
- **height/width**: Image dimensions (256-2048 pixels)
- **output_dir**: Directory to save generated images

## Example Usage Script

Run the example script to test the API:

```bash
python example_usage.py
```

This script demonstrates:
- Health check
- Image generation with different parameters
- Image download

## Error Handling

The service includes comprehensive error handling:
- CUDA availability checks
- GPU memory detection
- Model loading validation
- Generation error handling
- File system error handling

## Requirements

- Python 3.8+
- CUDA-capable GPU
- PyTorch with CUDA support
- See `requirements.txt` for complete dependency list

## Files

- `imagegeneration_final.py`: Core image generation functions
- `fastapi_service.py`: FastAPI web service
- `example_usage.py`: Example usage script
- `requirements.txt`: Python dependencies
- `README.md`: This documentation

## Docker Usage

### Building and Running

1. **Build the image:**
```bash
docker build -t stable-diffusion-api .
```

2. **Run with Docker Compose (recommended):**
```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

3. **Run with Docker directly:**
```bash
# Basic run
docker run --gpus all -p 8000:8000 stable-diffusion-api

# With volume mounting for persistent outputs
docker run --gpus all -p 8000:8000 \
  -v $(pwd)/final_outputs:/app/final_outputs \
  -v $(pwd)/upscaled_outputs:/app/upscaled_outputs \
  stable-diffusion-api
```

### Docker Environment Variables

You can customize the Docker container with environment variables:

```bash
docker run --gpus all -p 8000:8000 \
  -e NVIDIA_VISIBLE_DEVICES=0 \
  -e PYTHONUNBUFFERED=1 \
  stable-diffusion-api
```

### Volume Mounts

The Docker setup includes volume mounts for:
- `/app/final_outputs` - Generated images
- `/app/upscaled_outputs` - Upscaled images  
- `/app/scheduler_outputs` - Scheduler comparison images
- `/app/custom_upscaled` - Custom upscaled images

## Local Usage
