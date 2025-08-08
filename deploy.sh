#!/bin/bash

# Stable Diffusion API - Docker Deployment Script

set -e

echo "======================================"
echo "Stable Diffusion API - Docker Deploy"
echo "======================================"

# Configuration
IMAGE_NAME="stable-diffusion-api"
CONTAINER_NAME="stable-diffusion-api"
PORT="8000"

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "Error: Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "Warning: docker-compose is not installed. You can still use Docker directly."
    fi
}

# Function to check NVIDIA Docker runtime
check_nvidia_docker() {
    if ! docker info | grep -q nvidia; then
        echo "Warning: NVIDIA Docker runtime not detected."
        echo "Please install NVIDIA Container Toolkit for GPU support."
        echo "See: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html"
    else
        echo "✓ NVIDIA Docker runtime detected"
    fi
}

# Function to build the Docker image
build_image() {
    echo "Building Docker image: $IMAGE_NAME"
    docker build -t $IMAGE_NAME .
    echo "✓ Docker image built successfully"
}

# Function to run with docker-compose (recommended)
run_with_compose() {
    echo "Starting with docker-compose..."
    docker-compose up -d
    echo "✓ Service started with docker-compose"
    echo "API available at: http://localhost:$PORT"
    echo "API docs at: http://localhost:$PORT/docs"
}

# Function to run with Docker directly
run_with_docker() {
    echo "Starting with Docker directly..."
    
    # Stop existing container if running
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
    
    # Create volume directories
    mkdir -p final_outputs upscaled_outputs scheduler_outputs
    
    # Run the container
    docker run -d \
        --name $CONTAINER_NAME \
        --gpus all \
        -p $PORT:$PORT \
        -v $(pwd)/final_outputs:/app/final_outputs \
        -v $(pwd)/upscaled_outputs:/app/upscaled_outputs \
        -v $(pwd)/scheduler_outputs:/app/scheduler_outputs \
        $IMAGE_NAME
    
    echo "✓ Container started: $CONTAINER_NAME"
    echo "API available at: http://localhost:$PORT"
    echo "API docs at: http://localhost:$PORT/docs"
}

# Function to show logs
show_logs() {
    if command -v docker-compose &> /dev/null && [ -f "docker-compose.yml" ]; then
        docker-compose logs -f
    else
        docker logs -f $CONTAINER_NAME
    fi
}

# Function to stop the service
stop_service() {
    if command -v docker-compose &> /dev/null && [ -f "docker-compose.yml" ]; then
        echo "Stopping docker-compose services..."
        docker-compose down
    else
        echo "Stopping Docker container..."
        docker stop $CONTAINER_NAME 2>/dev/null || true
        docker rm $CONTAINER_NAME 2>/dev/null || true
    fi
    echo "✓ Service stopped"
}

# Function to test the deployment
test_deployment() {
    echo "Testing API deployment..."
    
    # Wait for service to start
    echo "Waiting for service to start..."
    sleep 10
    
    # Test health endpoint
    if curl -f http://localhost:$PORT/health > /dev/null 2>&1; then
        echo "✓ Health check passed"
    else
        echo "✗ Health check failed"
        return 1
    fi
    
    # Test generate endpoint with a simple request
    echo "Testing image generation..."
    curl -X POST "http://localhost:$PORT/generate" \
         -H "Content-Type: application/json" \
         -d '{
             "prompt": "a simple test image, digital art",
             "num_inference_steps": 10,
             "height": 512,
             "width": 512
         }' > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✓ Image generation test passed"
    else
        echo "✗ Image generation test failed"
        return 1
    fi
    
    echo "✓ All tests passed!"
}

# Main script logic
case "${1:-}" in
    "build")
        check_docker
        build_image
        ;;
    "start")
        check_docker
        check_nvidia_docker
        if command -v docker-compose &> /dev/null && [ -f "docker-compose.yml" ]; then
            run_with_compose
        else
            build_image
            run_with_docker
        fi
        ;;
    "logs")
        show_logs
        ;;
    "stop")
        stop_service
        ;;
    "test")
        test_deployment
        ;;
    "restart")
        stop_service
        sleep 2
        if command -v docker-compose &> /dev/null && [ -f "docker-compose.yml" ]; then
            run_with_compose
        else
            run_with_docker
        fi
        ;;
    "deploy")
        check_docker
        check_nvidia_docker
        build_image
        if command -v docker-compose &> /dev/null && [ -f "docker-compose.yml" ]; then
            run_with_compose
        else
            run_with_docker
        fi
        test_deployment
        ;;
    *)
        echo "Usage: $0 {build|start|stop|restart|logs|test|deploy}"
        echo ""
        echo "Commands:"
        echo "  build    - Build the Docker image"
        echo "  start    - Start the service"
        echo "  stop     - Stop the service"
        echo "  restart  - Restart the service"
        echo "  logs     - Show service logs"
        echo "  test     - Test the deployment"
        echo "  deploy   - Build, start, and test (full deployment)"
        echo ""
        echo "Examples:"
        echo "  $0 deploy          # Full deployment"
        echo "  $0 start           # Start service"
        echo "  $0 logs            # View logs"
        echo "  $0 test            # Test API"
        exit 1
        ;;
esac
