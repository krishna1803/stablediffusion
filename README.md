# Stable Diffusion Studio

A robust GPU-enabled Stable Diffusion service with FastAPI backend and Streamlit frontend, deployed via Docker with complete dependency isolation using Python 3.12 virtual environment.

## 🚀 Quick Start

```bash
# Clone and navigate to project
cd stablediffusion

# Deploy with Docker (Recommended)
./scripts/deploy.sh

# Or run locally
./scripts/run_local.sh
```

## 🌐 Access Services

- **Streamlit UI**: http://localhost:8501 (Main Interface)
- **FastAPI Backend**: http://localhost:8000 
- **Swagger API Docs**: http://localhost:8000/docs

## 📁 Project Structure

```
├── 📱 Main Services
│   ├── fastapi_service.py          # FastAPI backend with all endpoints
│   ├── streamlit_app.py            # Streamlit frontend interface
│   ├── imagegeneration_final.py    # Core image generation logic
│   ├── image_upscaling.py          # Image upscaling functionality
│   └── imagegeneration_schedulers.py # Scheduler management
├── 🐳 Docker & Deployment
│   ├── docker/
│   │   ├── Dockerfile              # Main container definition
│   │   ├── docker-compose.yml      # Multi-service orchestration
│   │   └── Dockerfile.alternative  # Backup configuration
│   └── scripts/
│       ├── deploy.sh               # Main deployment script
│       ├── start_studio.sh         # Service startup
│       ├── run_local.sh            # Local development
│       └── install_dependencies.sh # Dependency management
├── 📚 Documentation
│   ├── docs/
│   │   ├── README.md               # Comprehensive guide
│   │   ├── IMPLEMENTATION_SUMMARY.md
│   │   ├── VIRTUAL_ENVIRONMENT_SOLUTION.md
│   │   ├── DOCKER_BUILD_FIX.md
│   │   ├── STREAMLIT_GUIDE.md
│   │   ├── SWAGGER_UI_GUIDE.md
│   │   └── DEPENDENCY_TROUBLESHOOTING.md
├── 🧪 Testing & Examples
│   ├── tests/
│   │   ├── verify_project.py       # Project validation
│   │   ├── test_api.py            # API testing
│   │   └── test_venv_build.sh     # Docker build testing
│   └── examples/
│       ├── example_usage.py        # Usage examples
│       ├── upscaling_example.py    # Upscaling demos
│       └── scheduler_examples.py   # Scheduler demos
├── ⚙️ Configuration
│   └── config/
│       ├── requirements.txt        # Python dependencies
│       ├── requirements_clean.txt  # Minimal dependencies
│       └── environment.yaml        # Conda environment
└── 📂 Output Directories
    ├── final_outputs/              # Generated images
    ├── upscaled_outputs/           # Upscaled images
    └── scheduler_outputs/          # Scheduler test results
```

## ✨ Key Features

- **🎨 Image Generation**: Stable Diffusion with multiple models and schedulers
- **📈 Image Upscaling**: High-quality upscaling with Real-ESRGAN
- **🔧 Scheduler Testing**: Compare different sampling schedulers
- **🌐 Dual Interface**: Both API and web UI access
- **🐳 Docker Deployment**: GPU-enabled containerized deployment
- **🐍 Virtual Environment**: Isolated Python 3.12 environment
- **📊 Comprehensive Testing**: Full test suite and validation

## 📖 Documentation

For detailed information, please see the comprehensive documentation in the [`docs/`](docs/) folder:

- **[Complete README](docs/README.md)** - Full project documentation
- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)** - Technical overview
- **[Virtual Environment Solution](docs/VIRTUAL_ENVIRONMENT_SOLUTION.md)** - Dependency isolation approach
- **[Docker Build Guide](docs/DOCKER_BUILD_FIX.md)** - Container setup and troubleshooting
- **[Streamlit Guide](docs/STREAMLIT_GUIDE.md)** - Web interface usage
- **[API Documentation](docs/SWAGGER_UI_GUIDE.md)** - REST API reference

## 🔧 Requirements

- **Docker** with NVIDIA Container Toolkit (for GPU support)
- **NVIDIA GPU** with CUDA support (recommended)
- **Python 3.12+** (for local development)

## 🚀 Quick Commands

```bash
# Full deployment
./scripts/deploy.sh

# View logs
./scripts/deploy.sh logs

# Stop services
./scripts/deploy.sh stop

# Run tests
python tests/verify_project.py

# Local development
./scripts/run_local.sh
```

## 📝 License

This project is open source. See individual components for specific licensing.

---

**💡 For the complete documentation and advanced usage, please refer to [`docs/README.md`](docs/README.md)**
