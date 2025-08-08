"""
Example usage of the Stable Diffusion FastAPI service.

This script demonstrates how to:
1. Start the FastAPI server
2. Make requests to generate images
3. Download generated images

To run the FastAPI server:
    python fastapi_service.py

To make API requests:
    python example_usage.py
"""

import requests
import json
import time
import os

# API base URL (adjust if running on different host/port)
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.json()}")

def generate_image_api(prompt, **kwargs):
    """Generate an image using the API."""
    data = {
        "prompt": prompt,
        **kwargs
    }
    
    print(f"Generating image with prompt: '{prompt}'")
    response = requests.post(f"{BASE_URL}/generate", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Image generated successfully: {result['filename']}")
        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def download_image(filename, output_dir="final_outputs"):
    """Download a generated image."""
    params = {"output_dir": output_dir}
    response = requests.get(f"{BASE_URL}/download/{filename}", params=params)
    
    if response.status_code == 200:
        # Save the image locally
        local_filename = f"downloaded_{filename}"
        with open(local_filename, "wb") as f:
            f.write(response.content)
        print(f"Image downloaded as: {local_filename}")
        return local_filename
    else:
        print(f"Error downloading image: {response.status_code} - {response.text}")
        return None

def upscale_image_api(input_file, prompt, **kwargs):
    """Upscale a single image using the API."""
    data = {
        "input_file": input_file,
        "prompt": prompt,
        **kwargs
    }
    
    print(f"Upscaling image '{input_file}' with prompt: '{prompt}'")
    response = requests.post(f"{BASE_URL}/upscale", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Image upscaled successfully: {result['filename']}")
        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def upscale_directory_api(input_directory, prompt, **kwargs):
    """Upscale all images in a directory using the API."""
    data = {
        "input_directory": input_directory,
        "prompt": prompt,
        **kwargs
    }
    
    print(f"Upscaling directory '{input_directory}' with prompt: '{prompt}'")
    response = requests.post(f"{BASE_URL}/upscale-directory", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Directory upscaling completed: {result['successful_upscales']} images processed")
        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def upscale_highres_api(input_file, prompt, **kwargs):
    """Upscale an image with high resolution using the API."""
    data = {
        "input_file": input_file,
        "prompt": prompt,
        **kwargs
    }
    
    upscale_type = "8x (SD + SwinIR)" if kwargs.get("use_swinir", False) else "4x (SD only)"
    print(f"High-resolution upscaling ({upscale_type}) for '{input_file}' with prompt: '{prompt}'")
    response = requests.post(f"{BASE_URL}/upscale-highres", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"High-resolution upscaling completed: {result['filename']}")
        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def test_schedulers_api(prompt, schedulers_to_test=None, **kwargs):
    """Test multiple schedulers using the API."""
    data = {
        "prompt": prompt,
        "schedulers_to_test": schedulers_to_test,
        **kwargs
    }
    
    print(f"Testing schedulers with prompt: '{prompt}'")
    if schedulers_to_test:
        print(f"Testing specific schedulers: {schedulers_to_test}")
    else:
        print("Testing all available schedulers")
        
    response = requests.post(f"{BASE_URL}/test-schedulers", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Scheduler testing completed: {result['total_generated']} images generated")
        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def list_schedulers_api():
    """List available schedulers using the API."""
    response = requests.get(f"{BASE_URL}/schedulers")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Available schedulers ({result['total']}):")
        for scheduler in result['schedulers']:
            print(f"  - {scheduler}")
        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def generate_with_scheduler_api(prompt, scheduler_name, **kwargs):
    """Generate an image using a specific scheduler via the API."""
    data = {
        "prompt": prompt,
        "scheduler_name": scheduler_name,
        **kwargs
    }
    
    print(f"Generating image with scheduler '{scheduler_name}' and prompt: '{prompt}'")
    response = requests.post(f"{BASE_URL}/generate-scheduler", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Image generated successfully with {result['scheduler_used']}: {result['filename']}")
        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def list_files_api():
    """List all generated files via the API."""
    response = requests.get(f"{BASE_URL}/files")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Found {result['total_files']} generated files:")
        
        for directory, files in result['files'].items():
            if files:
                print(f"\n{directory}:")
                for file_info in files[:5]:  # Show first 5 files
                    print(f"  - {file_info['filename']} ({file_info['size_mb']} MB)")
                if len(files) > 5:
                    print(f"  ... and {len(files) - 5} more files")
            else:
                print(f"\n{directory}: No files")
        
        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def download_image_smart(filename):
    """Download an image by filename (automatically searches all directories)."""
    response = requests.get(f"{BASE_URL}/download/{filename}")
    
    if response.status_code == 200:
        # Save the image locally
        local_filename = f"downloaded_{filename}"
        with open(local_filename, "wb") as f:
            f.write(response.content)
        print(f"Image downloaded as: {local_filename}")
        return local_filename
    else:
        print(f"Error downloading image: {response.status_code} - {response.text}")
        return None

def main():
    """Main example function."""
    print("Testing Stable Diffusion FastAPI Service")
    print("=" * 50)
    
    # Test health endpoint
    try:
        test_health()
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the API server.")
        print("Make sure to start the server first: python fastapi_service.py")
        return
    
    # Example 1: Simple image generation
    print("\n1. Generating a simple image...")
    result1 = generate_image_api(
        prompt="a beautiful sunset over mountains, digital art",
        num_inference_steps=30,
        guidance_scale=7.5
    )
    
    if result1:
        print(f"Generated: {result1['output_path']}")
    
    # Example 2: Custom parameters
    print("\n2. Generating with custom parameters...")
    result2 = generate_image_api(
        prompt="a futuristic city with flying cars, cyberpunk style",
        negative_prompt="blurry, low quality, dark, ugly",
        num_inference_steps=40,
        guidance_scale=8.0,
        height=768,
        width=768
    )
    
    if result2:
        print(f"Generated: {result2['output_path']}")
        
        # Example 3: Upscale the generated image
        print("\n3. Upscaling the generated image...")
        upscale_result = upscale_image_api(
            input_file=result2['filename'],
            prompt="enhance details, high quality, sharp",
            num_inference_steps=50,
            guidance_scale=7.5
        )
        
        if upscale_result:
            print(f"Upscaled: {upscale_result['output_path']}")
            
            # Download the upscaled image
            print("Downloading the upscaled image...")
            downloaded_file = download_image(upscale_result['filename'])
            if downloaded_file:
                print(f"Downloaded to: {downloaded_file}")
    
    # Example 4: Generate with automatic upscaling
    print("\n4. Generating with automatic upscaling...")
    result4 = generate_image_api(
        prompt="a majestic dragon flying over ancient ruins",
        upscale=True,
        upscale_prompt="enhance details, photorealistic, high resolution",
        num_inference_steps=30
    )
    
    if result4:
        print(f"Generated and upscaled: {result4['output_path']}")
    
    # Example 5: List available schedulers
    print("\n5. Listing available schedulers...")
    scheduler_list = list_schedulers_api()
    
    # Example 6: Test specific schedulers
    print("\n6. Testing specific schedulers...")
    scheduler_result = test_schedulers_api(
        prompt="a beautiful sunset over the ocean, digital art",
        schedulers_to_test=["EulerDiscrete", "DPMSolverMultistep", "DDIM"],
        num_inference_steps=30,
        height=512,
        width=512,
        filename_prefix="sunset_comparison"
    )
    
    if scheduler_result:
        print("Scheduler test results:")
        for scheduler, path in scheduler_result['results'].items():
            print(f"  {scheduler}: {path}")
    
    # Example 7: Test high-resolution upscaling
    if result2:
        print("\n7. Testing high-resolution upscaling...")
        highres_result = upscale_highres_api(
            input_file=result2['filename'],
            prompt="ultra high resolution, sharp details, professional quality",
            sd_steps=50,
            sd_guidance_scale=8.0,
            use_swinir=False  # Set to True if you have SwinIR dependencies
        )
        
        if highres_result:
            print(f"High-res upscaling completed: {highres_result['output_path']}")
    
    # Example 8: Test directory upscaling (if you have a directory of images)
    print("\n8. Directory upscaling example (create a test directory first)...")
    test_dir = "test_images"
    if os.path.exists(test_dir):
        dir_result = upscale_directory_api(
            input_directory=test_dir,
            prompt="enhance details, improve quality",
            num_inference_steps=30,
            guidance_scale=7.0
        )
        
        if dir_result:
            print(f"Directory upscaling completed: {dir_result['successful_upscales']} images")
    else:
        print(f"Skipping directory upscaling (directory '{test_dir}' not found)")
    
    # Example 9: Test single scheduler generation
    print("\n9. Testing single scheduler generation...")
    single_scheduler_result = generate_with_scheduler_api(
        prompt="a majestic mountain landscape at sunset, digital art",
        scheduler_name="EulerDiscrete",
        num_inference_steps=30,
        guidance_scale=7.5,
        height=512,
        width=512
    )
    
    if single_scheduler_result:
        print(f"Single scheduler result: {single_scheduler_result['output_path']}")
    
    # Example 10: List all generated files
    print("\n10. Listing all generated files...")
    files_list = list_files_api()
    
    # Example 11: Smart download (automatically finds the file)
    if single_scheduler_result:
        print("\n11. Smart download of generated image...")
        downloaded_file = download_image_smart(single_scheduler_result['filename'])
        if downloaded_file:
            print(f"Downloaded: {downloaded_file}")
    
    # Example 12: Test with a different scheduler
    print("\n12. Testing with DPMSolverMultistep scheduler...")
    dpm_result = generate_with_scheduler_api(
        prompt="a futuristic city with neon lights, cyberpunk style",
        scheduler_name="DPMSolverMultistep",
        num_inference_steps=25,
        guidance_scale=8.0,
        height=768,
        width=768,
        filename_prefix="cyberpunk"
    )
    
    if dpm_result:
        print(f"DPM Solver result: {dpm_result['output_path']}")
    
    print("\n" + "="*50)
    print("All examples completed! Check the API docs at http://localhost:8000/docs")
    print("You can also list all files at: http://localhost:8000/files")

if __name__ == "__main__":
    main()
