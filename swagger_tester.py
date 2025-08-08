#!/usr/bin/env python3
"""
Swagger UI Testing Guide and Helper Script

This script helps you test the FastAPI service using Swagger UI instead of curl.
It also includes functions to test the API programmatically.
"""

import requests
import json
import time
import webbrowser
import sys
from typing import Dict, Any

class SwaggerUITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    def check_service_health(self) -> bool:
        """Check if the service is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Service is running and healthy")
                return True
            else:
                print(f"❌ Service health check failed: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to the service. Make sure it's running.")
            return False
        except Exception as e:
            print(f"❌ Error checking service: {e}")
            return False
    
    def open_swagger_ui(self):
        """Open Swagger UI in the default browser."""
        swagger_url = f"{self.base_url}/docs"
        print(f"🌐 Opening Swagger UI: {swagger_url}")
        
        try:
            webbrowser.open(swagger_url)
            print("✅ Swagger UI opened in your default browser")
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            print(f"Please manually open: {swagger_url}")
    
    def get_openapi_spec(self) -> Dict[str, Any]:
        """Get the OpenAPI specification."""
        try:
            response = requests.get(f"{self.base_url}/openapi.json")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Could not get OpenAPI spec: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Error getting OpenAPI spec: {e}")
            return {}
    
    def list_available_endpoints(self):
        """List all available endpoints from the OpenAPI spec."""
        spec = self.get_openapi_spec()
        if not spec:
            return
        
        print("\n📋 Available API Endpoints:")
        print("=" * 50)
        
        paths = spec.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE']:
                    summary = details.get('summary', 'No description')
                    print(f"🔸 {method.upper():6} {path:30} - {summary}")
        
        print(f"\nTotal endpoints: {sum(len(methods) for methods in paths.values())}")
    
    def test_basic_endpoints(self):
        """Test basic endpoints programmatically."""
        print("\n🧪 Testing Basic Endpoints:")
        print("=" * 50)
        
        # Test health endpoint
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ /health - OK")
            else:
                print(f"❌ /health - Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ /health - Error: {e}")
        
        # Test root endpoint
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("✅ / (root) - OK")
            else:
                print(f"❌ / (root) - Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ / (root) - Error: {e}")
        
        # Test schedulers endpoint
        try:
            response = requests.get(f"{self.base_url}/schedulers")
            if response.status_code == 200:
                data = response.json()
                scheduler_count = data.get('total', 0)
                print(f"✅ /schedulers - OK ({scheduler_count} schedulers available)")
            else:
                print(f"❌ /schedulers - Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ /schedulers - Error: {e}")
        
        # Test files endpoint
        try:
            response = requests.get(f"{self.base_url}/files")
            if response.status_code == 200:
                data = response.json()
                file_count = data.get('total_files', 0)
                print(f"✅ /files - OK ({file_count} files found)")
            else:
                print(f"❌ /files - Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ /files - Error: {e}")
    
    def show_swagger_usage_guide(self):
        """Show a guide on how to use Swagger UI."""
        print("\n📚 Swagger UI Usage Guide:")
        print("=" * 50)
        print("""
🎯 How to Use Swagger UI for Testing:

1. 📖 EXPLORE ENDPOINTS:
   • Click on any endpoint to expand it
   • View request/response schemas
   • See example values and descriptions

2. 🧪 TEST ENDPOINTS:
   • Click "Try it out" on any endpoint
   • Fill in required parameters
   • Click "Execute" to send the request
   • View the response in real-time

3. 🔍 COMMON TESTING SCENARIOS:

   A) Generate an Image:
      • Go to POST /generate
      • Click "Try it out"
      • Modify the request body:
        {
          "prompt": "a beautiful sunset over mountains",
          "num_inference_steps": 20,
          "height": 512,
          "width": 512
        }
      • Click "Execute"

   B) Test Schedulers:
      • First, check GET /schedulers to see available options
      • Then use POST /generate-scheduler:
        {
          "prompt": "cyberpunk city at night",
          "scheduler_name": "EulerDiscrete",
          "num_inference_steps": 25
        }

   C) List Generated Files:
      • Use GET /files to see all generated images
      • Copy a filename from the response

   D) Download an Image:
      • Use GET /download/{filename}
      • Paste the filename from step C
      • Click "Execute" and "Download" the result

4. 📋 RESPONSE FORMATS:
   • 200: Success - operation completed
   • 404: Not found - file/resource doesn't exist
   • 422: Validation error - check your input parameters
   • 500: Server error - check service logs

5. 💡 TIPS:
   • Use smaller values for testing (height=512, steps=10-20)
   • Start with simple prompts
   • Check /health if something seems wrong
   • View actual curl commands in the Swagger UI
        """)
    
    def generate_sample_requests(self):
        """Generate sample request examples for testing."""
        print("\n📝 Sample Requests for Swagger UI:")
        print("=" * 50)
        
        samples = {
            "Generate Image": {
                "endpoint": "POST /generate",
                "body": {
                    "prompt": "a beautiful landscape with mountains and a lake, digital art",
                    "negative_prompt": "blurry, low quality, ugly",
                    "num_inference_steps": 20,
                    "guidance_scale": 7.5,
                    "height": 512,
                    "width": 512,
                    "upscale": False
                }
            },
            "Generate with Scheduler": {
                "endpoint": "POST /generate-scheduler",
                "body": {
                    "prompt": "futuristic city with flying cars, cyberpunk style",
                    "scheduler_name": "EulerDiscrete",
                    "num_inference_steps": 25,
                    "guidance_scale": 8.0,
                    "height": 768,
                    "width": 768
                }
            },
            "Test Multiple Schedulers": {
                "endpoint": "POST /test-schedulers",
                "body": {
                    "prompt": "a serene forest path in autumn",
                    "schedulers_to_test": ["EulerDiscrete", "DDIM", "DPMSolverMultistep"],
                    "num_inference_steps": 20,
                    "filename_prefix": "forest_comparison"
                }
            }
        }
        
        for name, sample in samples.items():
            print(f"\n🔹 {name}:")
            print(f"   Endpoint: {sample['endpoint']}")
            print(f"   Request Body:")
            print(json.dumps(sample['body'], indent=4))

def main():
    """Main function."""
    print("🎨 Stable Diffusion API - Swagger UI Testing Helper")
    print("=" * 60)
    
    # Get API URL from command line or use default
    api_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    print(f"API URL: {api_url}")
    
    tester = SwaggerUITester(api_url)
    
    # Check if service is running
    if not tester.check_service_health():
        print("\n❌ Service is not running. Please start it first:")
        print("   ./deploy.sh deploy")
        print("   # or")
        print("   docker-compose up -d")
        print("   # or")
        print("   python3 fastapi_service.py")
        sys.exit(1)
    
    # Show menu
    while True:
        print("\n" + "=" * 60)
        print("🎯 What would you like to do?")
        print("=" * 60)
        print("1. 🌐 Open Swagger UI in browser")
        print("2. 📋 List all available endpoints")
        print("3. 🧪 Test basic endpoints")
        print("4. 📚 Show Swagger UI usage guide")
        print("5. 📝 Show sample requests")
        print("6. 🔍 Get OpenAPI specification")
        print("7. ❌ Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            tester.open_swagger_ui()
            print("\n💡 Use the browser to test your API interactively!")
            
        elif choice == "2":
            tester.list_available_endpoints()
            
        elif choice == "3":
            tester.test_basic_endpoints()
            
        elif choice == "4":
            tester.show_swagger_usage_guide()
            
        elif choice == "5":
            tester.generate_sample_requests()
            
        elif choice == "6":
            spec = tester.get_openapi_spec()
            if spec:
                print("\n📄 OpenAPI Specification:")
                print(json.dumps(spec, indent=2)[:1000] + "..." if len(str(spec)) > 1000 else json.dumps(spec, indent=2))
            
        elif choice == "7":
            print("\n👋 Goodbye! Happy testing!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-7.")

if __name__ == "__main__":
    main()
