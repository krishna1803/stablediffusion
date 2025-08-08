#!/usr/bin/env python3
"""
File Verification Script for Stable Diffusion Service

This script checks all project files for common issues and validates the setup.
"""

import os
import json
import sys
from pathlib import Path

class ProjectVerifier:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.issues = []
        self.warnings = []
        
    def log_issue(self, issue: str):
        """Log a critical issue."""
        self.issues.append(issue)
        print(f"❌ ISSUE: {issue}")
        
    def log_warning(self, warning: str):
        """Log a warning."""
        self.warnings.append(warning)
        print(f"⚠️  WARNING: {warning}")
        
    def log_success(self, message: str):
        """Log a success message."""
        print(f"✅ {message}")
    
    def check_required_files(self):
        """Check if all required files exist."""
        print("\n📁 Checking Required Files...")
        
        required_files = [
            "fastapi_service.py",
            "streamlit_app.py",
            "imagegeneration_final.py", 
            "image_upscaling.py",
            "imagegeneration_schedulers.py",
            "requirements.txt",
            "install_dependencies.sh",
            "fix_dependencies.sh", 
            "Dockerfile",
            "docker-compose.yml",
            "deploy.sh",
            "run_local.sh",
            "start_studio.sh",
            "test_api.py",
            "README.md"
        ]
        
        for file in required_files:
            file_path = self.project_dir / file
            if file_path.exists():
                self.log_success(f"Found {file}")
            else:
                self.log_issue(f"Missing required file: {file}")
    
    def check_python_syntax(self):
        """Check Python files for syntax errors."""
        print("\n🐍 Checking Python Syntax...")
        
        python_files = [
            "fastapi_service.py",
            "imagegeneration_final.py",
            "image_upscaling.py", 
            "imagegeneration_schedulers.py",
            "example_usage.py",
            "test_api.py",
            "comprehensive_upscaling_example.py",
            "scheduler_examples.py",
            "upscaling_example.py"
        ]
        
        for file in python_files:
            file_path = self.project_dir / file
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    compile(content, file, 'exec')
                    self.log_success(f"Python syntax OK: {file}")
                except SyntaxError as e:
                    self.log_issue(f"Syntax error in {file}: {e}")
                except Exception as e:
                    self.log_warning(f"Could not check {file}: {e}")
            else:
                self.log_warning(f"Python file not found: {file}")
    
    def check_docker_files(self):
        """Check Docker configuration files."""
        print("\n🐳 Checking Docker Configuration...")
        
        # Check Dockerfile
        dockerfile_path = self.project_dir / "Dockerfile"
        if dockerfile_path.exists():
            with open(dockerfile_path, 'r') as f:
                content = f.read()
            
            if "nvidia/cuda" in content:
                self.log_success("Dockerfile uses NVIDIA CUDA base image")
            else:
                self.log_warning("Dockerfile doesn't use NVIDIA CUDA base image")
                
            if "python3.12" in content:
                self.log_success("Dockerfile installs Python 3.12")
            else:
                self.log_warning("Dockerfile doesn't explicitly install Python 3.12")
                
            if "update-alternatives" in content and "python3.12" in content:
                self.log_success("Dockerfile sets Python 3.12 as default")
            else:
                self.log_warning("Dockerfile doesn't set Python 3.12 as default")
                
            if "start_studio.sh" in content or "streamlit" in content:
                self.log_success("Dockerfile configured for Streamlit UI")
            else:
                self.log_warning("Dockerfile doesn't include Streamlit configuration")
                
            if "EXPOSE 8000" in content or "8000" in content:
                self.log_success("Dockerfile exposes port 8000 (FastAPI)")
            else:
                self.log_warning("Dockerfile doesn't expose port 8000")
                
            if "EXPOSE 8501" in content or "8501" in content:
                self.log_success("Dockerfile exposes port 8501 (Streamlit)")
            else:
                self.log_warning("Dockerfile doesn't expose port 8501")
        
        # Check docker-compose.yml
        compose_path = self.project_dir / "docker-compose.yml"
        if compose_path.exists():
            try:
                import yaml
                with open(compose_path, 'r') as f:
                    compose_config = yaml.safe_load(f)
                
                services = compose_config.get('services', {})
                if services:
                    service_name = list(services.keys())[0]
                    service = services[service_name]
                    
                    if 'deploy' in service and 'resources' in service['deploy']:
                        self.log_success("Docker Compose has GPU resource configuration")
                    else:
                        self.log_warning("Docker Compose missing GPU configuration")
                        
                    ports = service.get('ports', [])
                    if any('8000:8000' in str(port) for port in ports):
                        self.log_success("Docker Compose exposes port 8000")
                    else:
                        self.log_issue("Docker Compose doesn't expose port 8000")
                        
                self.log_success("Docker Compose file is valid YAML")
            except ImportError:
                self.log_warning("PyYAML not available - skipping docker-compose validation")
            except Exception as e:
                self.log_issue(f"Docker Compose file error: {e}")
    
    def check_requirements(self):
        """Check requirements.txt."""
        print("\n📦 Checking Requirements...")
        
        req_path = self.project_dir / "requirements.txt"
        if req_path.exists():
            with open(req_path, 'r') as f:
                requirements = f.read()
            
            required_packages = [
                'torch',
                'diffusers', 
                'fastapi',
                'uvicorn',
                'pydantic',
                'requests',
                'pillow',
                'streamlit'
            ]
            
            for package in required_packages:
                if package.lower() in requirements.lower():
                    self.log_success(f"Required package found: {package}")
                else:
                    self.log_issue(f"Missing required package: {package}")
    
    def check_scripts_executable(self):
        """Check if scripts are executable."""
        print("\n🔧 Checking Script Permissions...")
        
        scripts = ["deploy.sh", "start.sh", "test_api.py"]
        
        for script in scripts:
            script_path = self.project_dir / script
            if script_path.exists():
                if os.access(script_path, os.X_OK):
                    self.log_success(f"Script is executable: {script}")
                else:
                    self.log_warning(f"Script not executable: {script} (run: chmod +x {script})")
            else:
                self.log_warning(f"Script not found: {script}")
    
    def check_api_endpoints(self):
        """Check FastAPI service for endpoint definitions."""
        print("\n🌐 Checking API Endpoints...")
        
        fastapi_path = self.project_dir / "fastapi_service.py"
        if fastapi_path.exists():
            with open(fastapi_path, 'r') as f:
                content = f.read()
            
            expected_endpoints = [
                '@app.post("/generate"',
                '@app.post("/upscale"',
                '@app.post("/upscale-directory"',
                '@app.post("/upscale-highres"',
                '@app.post("/test-schedulers"',
                '@app.get("/schedulers"',
                '@app.get("/download/',
                '@app.get("/health"',
                '@app.get("/"'
            ]
            
            for endpoint in expected_endpoints:
                if endpoint in content:
                    self.log_success(f"Endpoint found: {endpoint}")
                else:
                    self.log_issue(f"Missing endpoint: {endpoint}")
    
    def check_output_directories(self):
        """Check if output directories exist or can be created."""
        print("\n📂 Checking Output Directories...")
        
        directories = [
            "final_outputs",
            "upscaled_outputs", 
            "scheduler_outputs"
        ]
        
        for directory in directories:
            dir_path = self.project_dir / directory
            try:
                dir_path.mkdir(exist_ok=True)
                self.log_success(f"Output directory ready: {directory}")
            except Exception as e:
                self.log_issue(f"Cannot create directory {directory}: {e}")
    
    def check_swagger_ui(self):
        """Check if Swagger UI endpoints are properly configured."""
        print("\n📚 Checking Swagger UI Configuration...")
        
        fastapi_path = self.project_dir / "fastapi_service.py"
        if fastapi_path.exists():
            with open(fastapi_path, 'r') as f:
                content = f.read()
            
            # Check for FastAPI instance with proper configuration
            if 'FastAPI(' in content and 'title=' in content:
                self.log_success("FastAPI app configured with title")
            else:
                self.log_warning("FastAPI app missing title configuration")
            
            # Check for proper Pydantic models (required for Swagger documentation)
            if 'BaseModel' in content and 'Field(' in content:
                self.log_success("Pydantic models properly configured for Swagger")
            else:
                self.log_issue("Missing Pydantic models or Field descriptions")
            
            # Check for response models in endpoints
            if 'response_model=' in content:
                self.log_success("Endpoints have response models for Swagger documentation")
            else:
                self.log_warning("Some endpoints may be missing response models")
            
            # Check for proper docstrings
            docstring_count = content.count('"""')
            if docstring_count >= 10:  # Expect at least 5 endpoints with docstrings
                self.log_success("Endpoints have documentation strings")
            else:
                self.log_warning("Some endpoints may be missing documentation")
        
        self.log_success("Swagger UI will be available at /docs")
        self.log_success("ReDoc will be available at /redoc")
    
    def check_docker_image_availability(self):
        """Check if the Docker base image is available."""
        print("\n🐳 Checking Docker Image Availability...")
        
        dockerfile_path = self.project_dir / "Dockerfile"
        if dockerfile_path.exists():
            with open(dockerfile_path, 'r') as f:
                content = f.read()
            
            # Extract the base image from Dockerfile
            for line in content.split('\n'):
                if line.strip().startswith('FROM '):
                    base_image = line.strip().replace('FROM ', '')
                    self.log_success(f"Base image configured: {base_image}")
                    
                    # Check if it's a NVIDIA CUDA image
                    if 'nvidia/cuda' in base_image:
                        self.log_success("Using NVIDIA CUDA base image")
                        if 'devel' in base_image:
                            self.log_success("Using development image (includes build tools)")
                        elif 'runtime' in base_image:
                            self.log_success("Using runtime image (smaller size)")
                    else:
                        self.log_warning("Not using NVIDIA CUDA base image")
                    
                    break
            else:
                self.log_issue("No FROM statement found in Dockerfile")
            
            # Check for GPU-related environment variables
            if 'NVIDIA_VISIBLE_DEVICES' in content:
                self.log_success("NVIDIA GPU environment variables configured")
            else:
                self.log_warning("Missing NVIDIA GPU environment variables")
        
        # Check if troubleshooting script exists
        troubleshoot_script = self.project_dir / "docker_troubleshoot.sh"
        if troubleshoot_script.exists():
            self.log_success("Docker troubleshooting script available")
        else:
            self.log_warning("Docker troubleshooting script not found")
    
    def run_verification(self):
        """Run all verification checks."""
        print("🔍 Project Verification Starting...")
        print("=" * 50)
        
        self.check_required_files()
        self.check_python_syntax()
        self.check_docker_files()
        self.check_docker_image_availability()
        self.check_requirements()
        self.check_scripts_executable()
        self.check_api_endpoints()
        self.check_swagger_ui()
        self.check_output_directories()
        
        print("\n" + "=" * 50)
        print("📋 VERIFICATION SUMMARY")
        print("=" * 50)
        
        if not self.issues and not self.warnings:
            print("🎉 All checks passed! Project is ready for deployment.")
            return True
        
        if self.issues:
            print(f"❌ Found {len(self.issues)} critical issues:")
            for issue in self.issues:
                print(f"   • {issue}")
        
        if self.warnings:
            print(f"⚠️  Found {len(self.warnings)} warnings:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.issues:
            print("\n🔧 Fix critical issues before deployment.")
            return False
        else:
            print("\n✅ No critical issues found. Warnings can be addressed optionally.")
            return True

def main():
    """Main function."""
    project_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    verifier = ProjectVerifier(project_dir)
    success = verifier.run_verification()
    
    if not success:
        sys.exit(1)
    else:
        print("\n🚀 Project verification complete - ready for deployment!")
        sys.exit(0)

if __name__ == "__main__":
    main()
