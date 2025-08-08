#!/usr/bin/env python3
"""
Comprehensive API Test Suite for Stable Diffusion Service

This script tests all endpoints and functionality of the API.
"""

import requests
import json
import time
import os
import sys
from typing import Dict, Any, List

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test results."""
        status = "✓" if success else "✗"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
        
    def test_health(self) -> bool:
        """Test health endpoint."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                self.log_test("Health Check", True, "API is healthy")
                return True
            else:
                self.log_test("Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {e}")
            return False
    
    def test_root_endpoint(self) -> bool:
        """Test root endpoint."""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Root Endpoint", True, f"Version: {data.get('version', 'N/A')}")
                return True
            else:
                self.log_test("Root Endpoint", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Error: {e}")
            return False
    
    def test_list_schedulers(self) -> bool:
        """Test scheduler listing."""
        try:
            response = requests.get(f"{self.base_url}/schedulers", timeout=10)
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('schedulers', []))
                self.log_test("List Schedulers", True, f"Found {count} schedulers")
                return True
            else:
                self.log_test("List Schedulers", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("List Schedulers", False, f"Error: {e}")
            return False
    
    def test_image_generation(self) -> Dict[str, Any]:
        """Test basic image generation."""
        try:
            payload = {
                "prompt": "a simple test image, digital art",
                "num_inference_steps": 10,
                "guidance_scale": 7.0,
                "height": 512,
                "width": 512
            }
            
            response = requests.post(
                f"{self.base_url}/generate", 
                json=payload, 
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                filename = data.get('filename', '')
                self.log_test("Image Generation", True, f"Generated: {filename}")
                return data
            else:
                self.log_test("Image Generation", False, f"Status: {response.status_code}")
                return {}
        except Exception as e:
            self.log_test("Image Generation", False, f"Error: {e}")
            return {}
    
    def test_image_generation_with_upscaling(self) -> Dict[str, Any]:
        """Test image generation with automatic upscaling."""
        try:
            payload = {
                "prompt": "a beautiful landscape, digital art",
                "num_inference_steps": 15,
                "guidance_scale": 7.5,
                "height": 512,
                "width": 512,
                "upscale": True,
                "upscale_prompt": "enhance details, high quality"
            }
            
            response = requests.post(
                f"{self.base_url}/generate", 
                json=payload, 
                timeout=180
            )
            
            if response.status_code == 200:
                data = response.json()
                filename = data.get('filename', '')
                self.log_test("Generation + Upscaling", True, f"Generated and upscaled: {filename}")
                return data
            else:
                self.log_test("Generation + Upscaling", False, f"Status: {response.status_code}")
                return {}
        except Exception as e:
            self.log_test("Generation + Upscaling", False, f"Error: {e}")
            return {}
    
    def test_upscaling(self, test_filename: str) -> bool:
        """Test single image upscaling."""
        if not test_filename:
            self.log_test("Single Upscaling", False, "No test image available")
            return False
            
        try:
            payload = {
                "input_file": test_filename,
                "prompt": "enhance details, improve quality",
                "num_inference_steps": 30,
                "guidance_scale": 7.5
            }
            
            response = requests.post(
                f"{self.base_url}/upscale", 
                json=payload, 
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                filename = data.get('filename', '')
                self.log_test("Single Upscaling", True, f"Upscaled: {filename}")
                return True
            else:
                self.log_test("Single Upscaling", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Single Upscaling", False, f"Error: {e}")
            return False
    
    def test_high_res_upscaling(self, test_filename: str) -> bool:
        """Test high-resolution upscaling."""
        if not test_filename:
            self.log_test("High-Res Upscaling", False, "No test image available")
            return False
            
        try:
            payload = {
                "input_file": test_filename,
                "prompt": "ultra high resolution, sharp details",
                "sd_steps": 40,
                "sd_guidance_scale": 8.0,
                "use_swinir": False  # Set to True if SwinIR is available
            }
            
            response = requests.post(
                f"{self.base_url}/upscale-highres", 
                json=payload, 
                timeout=150
            )
            
            if response.status_code == 200:
                data = response.json()
                filename = data.get('filename', '')
                self.log_test("High-Res Upscaling", True, f"High-res upscaled: {filename}")
                return True
            else:
                self.log_test("High-Res Upscaling", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("High-Res Upscaling", False, f"Error: {e}")
            return False
    
    def test_scheduler_comparison(self) -> bool:
        """Test scheduler comparison."""
        try:
            payload = {
                "prompt": "a test image for scheduler comparison",
                "schedulers_to_test": ["EulerDiscrete", "DDIM"],
                "num_inference_steps": 20,
                "guidance_scale": 7.0,
                "height": 512,
                "width": 512,
                "filename_prefix": "test_scheduler"
            }
            
            response = requests.post(
                f"{self.base_url}/test-schedulers", 
                json=payload, 
                timeout=180
            )
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('total_generated', 0)
                self.log_test("Scheduler Comparison", True, f"Generated {count} images")
                return True
            else:
                self.log_test("Scheduler Comparison", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Scheduler Comparison", False, f"Error: {e}")
            return False
    
    def test_file_download(self, filename: str) -> bool:
        """Test file download."""
        if not filename:
            self.log_test("File Download", False, "No filename provided")
            return False
            
        try:
            response = requests.get(
                f"{self.base_url}/download/{filename}", 
                timeout=30
            )
            
            if response.status_code == 200:
                size = len(response.content)
                self.log_test("File Download", True, f"Downloaded {size} bytes")
                return True
            else:
                self.log_test("File Download", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("File Download", False, f"Error: {e}")
            return False
    
    def test_single_scheduler_generation(self) -> bool:
        """Test single scheduler image generation."""
        try:
            data = {
                "prompt": "a simple test image for scheduler testing",
                "scheduler_name": "EulerDiscrete",
                "num_inference_steps": 10,
                "guidance_scale": 7.0,
                "height": 512,
                "width": 512,
                "filename_prefix": "api_test"
            }
            
            response = requests.post(f"{self.base_url}/generate-scheduler", json=data, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                filename = result.get('filename', '')
                scheduler_used = result.get('scheduler_used', '')
                self.log_test("Single Scheduler Generation", True, 
                            f"Generated {filename} with {scheduler_used}")
                return True
            else:
                self.log_test("Single Scheduler Generation", False, 
                            f"Status: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            self.log_test("Single Scheduler Generation", False, "Request timeout (>120s)")
            return False
        except Exception as e:
            self.log_test("Single Scheduler Generation", False, f"Error: {e}")
            return False
    
    def test_files_listing(self) -> bool:
        """Test files listing endpoint."""
        try:
            response = requests.get(f"{self.base_url}/files", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                total_files = result.get('total_files', 0)
                self.log_test("Files Listing", True, f"Found {total_files} files")
                return True
            else:
                self.log_test("Files Listing", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Files Listing", False, f"Error: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests."""
        print("Starting Comprehensive API Test Suite")
        print("=" * 50)
        
        start_time = time.time()
        
        # Basic connectivity tests
        if not self.test_health():
            print("❌ Health check failed - stopping tests")
            return self.get_results()
        
        self.test_root_endpoint()
        self.test_list_schedulers()
        
        # Image generation tests
        gen_result = self.test_image_generation()
        test_filename = gen_result.get('filename', '')
        
        # Test upscaling if we have a generated image
        if test_filename:
            self.test_upscaling(test_filename)
            self.test_high_res_upscaling(test_filename)
            self.test_file_download(test_filename)
        
        # Advanced tests
        self.test_image_generation_with_upscaling()
        self.test_scheduler_comparison()
        self.test_single_scheduler_generation()
        self.test_files_listing()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\nTest suite completed in {duration:.1f} seconds")
        return self.get_results()
    
    def get_results(self) -> Dict[str, Any]:
        """Get test results summary."""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "results": self.test_results
        }
    
    def print_summary(self):
        """Print test summary."""
        results = self.get_results()
        
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {results['total_tests']}")
        print(f"Passed: {results['passed']}")
        print(f"Failed: {results['failed']}")
        print(f"Success Rate: {results['success_rate']:.1f}%")
        
        if results['failed'] > 0:
            print("\nFailed Tests:")
            for result in results['results']:
                if not result['success']:
                    print(f"  ❌ {result['test']}: {result['message']}")
        
        print("=" * 50)

def main():
    """Main function."""
    # Check if API URL is provided
    api_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"Testing API at: {api_url}")
    
    # Create tester instance
    tester = APITester(api_url)
    
    # Run tests
    results = tester.run_all_tests()
    
    # Print summary
    tester.print_summary()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        sys.exit(1)
    else:
        print("🎉 All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
