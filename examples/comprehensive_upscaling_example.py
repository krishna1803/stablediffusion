"""
Comprehensive upscaling examples demonstrating all three upscaling methods.

This script shows how to:
1. Upscale a single image
2. Upscale all images in a directory
3. Perform high-resolution upscaling (4x or 8x)
"""

from image_upscaling import upscale_image, upscale_directory, upscale_high_resolution, initialize_upscale_pipeline
import os

def create_test_directory():
    """Create a test directory with some sample images for testing."""
    test_dir = "test_images_for_upscaling"
    os.makedirs(test_dir, exist_ok=True)
    
    # Check if we have any existing images to copy for testing
    source_dirs = ["final_outputs", "scheduler_outputs", "outputs"]
    
    copied_files = 0
    for source_dir in source_dirs:
        if os.path.exists(source_dir):
            for file in os.listdir(source_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    source_path = os.path.join(source_dir, file)
                    dest_path = os.path.join(test_dir, f"test_{copied_files}_{file}")
                    
                    # Copy the file (simple copy for testing)
                    try:
                        import shutil
                        shutil.copy2(source_path, dest_path)
                        copied_files += 1
                        if copied_files >= 3:  # Limit to 3 files for testing
                            break
                    except Exception as e:
                        print(f"Could not copy {source_path}: {e}")
        
        if copied_files >= 3:
            break
    
    if copied_files > 0:
        print(f"Created test directory '{test_dir}' with {copied_files} test images")
        return test_dir
    else:
        print(f"Could not create test images in '{test_dir}' - no source images found")
        return None

def example_single_image_upscaling():
    """Example of upscaling a single image."""
    print("=== Single Image Upscaling Example ===")
    
    # Look for an existing image to upscale
    test_image = None
    search_dirs = ["final_outputs", "scheduler_outputs", "outputs"]
    
    for search_dir in search_dirs:
        if os.path.exists(search_dir):
            for file in os.listdir(search_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    test_image = os.path.join(search_dir, file)
                    break
        if test_image:
            break
    
    if not test_image:
        print("No test image found. Please generate an image first or provide an image path.")
        return
    
    print(f"Upscaling image: {test_image}")
    
    try:
        upscaled_path = upscale_image(
            input_file=test_image,
            prompt="enhance details, improve quality, sharp and clear",
            num_inference_steps=50,
            guidance_scale=7.5,
            output_dir="single_upscale_test"
        )
        print(f"✓ Single image upscaling completed: {upscaled_path}")
        
    except Exception as e:
        print(f"✗ Error in single image upscaling: {e}")

def example_directory_upscaling():
    """Example of upscaling all images in a directory."""
    print("\n=== Directory Upscaling Example ===")
    
    # Create or use existing test directory
    test_dir = create_test_directory()
    
    if not test_dir:
        print("Skipping directory upscaling - no test directory available")
        return
    
    try:
        upscaled_paths = upscale_directory(
            input_directory=test_dir,
            prompt="enhance all details, improve image quality",
            output_directory="directory_upscale_test",
            num_inference_steps=40,
            guidance_scale=7.0
        )
        
        print(f"✓ Directory upscaling completed: {len(upscaled_paths)} images processed")
        for path in upscaled_paths:
            print(f"  - {path}")
            
    except Exception as e:
        print(f"✗ Error in directory upscaling: {e}")

def example_high_resolution_upscaling():
    """Example of high-resolution upscaling."""
    print("\n=== High-Resolution Upscaling Example ===")
    
    # Look for an existing image to upscale
    test_image = None
    search_dirs = ["final_outputs", "scheduler_outputs", "outputs"]
    
    for search_dir in search_dirs:
        if os.path.exists(search_dir):
            for file in os.listdir(search_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    test_image = os.path.join(search_dir, file)
                    break
        if test_image:
            break
    
    if not test_image:
        print("No test image found. Please generate an image first or provide an image path.")
        return
    
    print(f"High-resolution upscaling image: {test_image}")
    
    # Test 4x upscaling (SD only)
    try:
        print("Testing 4x upscaling (Stable Diffusion only)...")
        upscaled_4x_path = upscale_high_resolution(
            input_file=test_image,
            prompt="ultra high resolution, photorealistic, extreme detail",
            output_dir="highres_upscale_test",
            sd_steps=60,
            sd_guidance_scale=8.0,
            use_swinir=False
        )
        print(f"✓ 4x high-resolution upscaling completed: {upscaled_4x_path}")
        
    except Exception as e:
        print(f"✗ Error in 4x upscaling: {e}")
    
    # Test 8x upscaling (SD + SwinIR)
    try:
        print("Testing 8x upscaling (Stable Diffusion + SwinIR)...")
        upscaled_8x_path = upscale_high_resolution(
            input_file=test_image,
            prompt="ultra high resolution, photorealistic, extreme detail",
            output_dir="highres_upscale_test",
            sd_steps=60,
            sd_guidance_scale=8.0,
            use_swinir=True
        )
        print(f"✓ 8x high-resolution upscaling completed: {upscaled_8x_path}")
        
    except Exception as e:
        print(f"✗ Error in 8x upscaling: {e}")

def example_custom_parameters():
    """Example with custom parameters for different use cases."""
    print("\n=== Custom Parameters Example ===")
    
    # Look for an existing image
    test_image = None
    search_dirs = ["final_outputs", "scheduler_outputs", "outputs"]
    
    for search_dir in search_dirs:
        if os.path.exists(search_dir):
            for file in os.listdir(search_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    test_image = os.path.join(search_dir, file)
                    break
        if test_image:
            break
    
    if not test_image:
        print("No test image found for custom parameters example.")
        return
    
    # Test different parameter combinations
    test_configs = [
        {
            "name": "high_quality",
            "steps": 80,
            "guidance": 8.5,
            "prompt": "masterpiece, ultra high quality, photorealistic, sharp details"
        },
        {
            "name": "fast_upscale", 
            "steps": 25,
            "guidance": 6.0,
            "prompt": "improve quality, enhance details"
        },
        {
            "name": "artistic_enhance",
            "steps": 60,
            "guidance": 9.0,
            "prompt": "artistic masterpiece, beautiful composition, enhanced colors"
        }
    ]
    
    for config in test_configs:
        try:
            print(f"Testing {config['name']} configuration...")
            
            upscaled_path = upscale_image(
                input_file=test_image,
                prompt=config["prompt"],
                num_inference_steps=config["steps"],
                guidance_scale=config["guidance"],
                output_dir="custom_params_test",
                output_file=f"test_{config['name']}_upscaled.png"
            )
            
            print(f"✓ {config['name']} upscaling completed: {upscaled_path}")
            
        except Exception as e:
            print(f"✗ Error with {config['name']} configuration: {e}")

def main():
    """Main function to run all upscaling examples."""
    print("Comprehensive Upscaling Examples")
    print("=" * 50)
    
    # Initialize the upscaling pipeline
    try:
        print("Initializing upscaling pipeline...")
        initialize_upscale_pipeline()
        print("✓ Pipeline initialized successfully!\n")
    except Exception as e:
        print(f"✗ Error initializing pipeline: {e}")
        return
    
    # Run all examples
    example_single_image_upscaling()
    example_directory_upscaling()
    example_high_resolution_upscaling()
    example_custom_parameters()
    
    print("\n" + "=" * 50)
    print("All upscaling examples completed!")
    print("Check the following directories for results:")
    print("  - single_upscale_test/")
    print("  - directory_upscale_test/")
    print("  - highres_upscale_test/")
    print("  - custom_params_test/")

if __name__ == "__main__":
    main()
