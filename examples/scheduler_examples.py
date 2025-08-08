"""
Example usage of the scheduler testing functionality.

This script demonstrates how to:
1. Use the scheduler testing function directly in Python code
2. Test specific schedulers
3. Compare different schedulers with the same prompt
"""

from imagegeneration_schedulers import generate_images_with_schedulers, initialize_pipeline, SCHEDULERS

def example_test_all_schedulers():
    """Example of testing all available schedulers."""
    
    print("=== Testing All Schedulers ===")
    
    prompt = "a beautiful mountain landscape at sunset, digital art, highly detailed"
    
    try:
        results = generate_images_with_schedulers(
            prompt=prompt,
            num_inference_steps=50,  # Reduced steps for faster testing
            guidance_scale=7.5,
            height=768,
            width=768,
            filename_prefix="landscape_test"
        )
        
        print(f"\nSuccessfully generated {len(results)} images:")
        for scheduler, path in results.items():
            print(f"  {scheduler}: {path}")
            
    except Exception as e:
        print(f"Error testing schedulers: {e}")

def example_test_specific_schedulers():
    """Example of testing specific schedulers."""
    
    print("\n=== Testing Specific Schedulers ===")
    
    # Test only a few fast schedulers
    fast_schedulers = ["EulerDiscrete", "DPMSolverMultistep", "DDIM", "PNDM"]
    
    prompt = "a futuristic robot in a cyberpunk city, neon lights, detailed"
    
    try:
        results = generate_images_with_schedulers(
            prompt=prompt,
            schedulers_to_test=fast_schedulers,
            num_inference_steps=30,
            guidance_scale=8.0,
            height=512,
            width=512,
            output_dir="scheduler_comparison",
            filename_prefix="robot_cyberpunk"
        )
        
        print(f"\nSuccessfully generated {len(results)} images with fast schedulers:")
        for scheduler, path in results.items():
            print(f"  {scheduler}: {path}")
            
    except Exception as e:
        print(f"Error testing specific schedulers: {e}")

def example_quality_comparison():
    """Example comparing quality-focused vs speed-focused schedulers."""
    
    print("\n=== Quality vs Speed Comparison ===")
    
    # Quality-focused schedulers (more steps, better quality)
    quality_schedulers = ["DDIM", "DPMSolverMultistep", "HeunDiscrete"]
    
    # Speed-focused schedulers (fewer steps, faster generation)
    speed_schedulers = ["LCM", "EulerDiscrete", "DPMSolverSinglestep"]
    
    prompt = "a portrait of an elegant woman in renaissance style, oil painting"
    
    # Test quality schedulers with more steps
    print("Testing quality-focused schedulers (more steps)...")
    try:
        quality_results = generate_images_with_schedulers(
            prompt=prompt,
            schedulers_to_test=quality_schedulers,
            num_inference_steps=80,
            guidance_scale=7.5,
            height=768,
            width=768,
            output_dir="quality_comparison",
            filename_prefix="portrait_quality"
        )
        print(f"Quality schedulers completed: {len(quality_results)} images")
    except Exception as e:
        print(f"Error with quality schedulers: {e}")
    
    # Test speed schedulers with fewer steps
    print("Testing speed-focused schedulers (fewer steps)...")
    try:
        speed_results = generate_images_with_schedulers(
            prompt=prompt,
            schedulers_to_test=speed_schedulers,
            num_inference_steps=20,
            guidance_scale=7.5,
            height=768,
            width=768,
            output_dir="speed_comparison",
            filename_prefix="portrait_speed"
        )
        print(f"Speed schedulers completed: {len(speed_results)} images")
    except Exception as e:
        print(f"Error with speed schedulers: {e}")

def list_available_schedulers():
    """List all available schedulers."""
    
    print("\n=== Available Schedulers ===")
    print(f"Total schedulers available: {len(SCHEDULERS)}")
    
    for i, scheduler_name in enumerate(SCHEDULERS.keys(), 1):
        print(f"{i:2d}. {scheduler_name}")

def example_custom_parameters():
    """Example with custom parameters for specific use cases."""
    
    print("\n=== Custom Parameters Example ===")
    
    # Test with different image sizes and steps
    test_configs = [
        {
            "name": "high_res",
            "schedulers": ["DPMSolverMultistep", "EulerDiscrete"],
            "height": 1024,
            "width": 1024,
            "steps": 60
        },
        {
            "name": "quick_preview",
            "schedulers": ["LCM", "EulerDiscrete"],
            "height": 512,
            "width": 512,
            "steps": 15
        }
    ]
    
    prompt = "a magical forest with glowing mushrooms, fantasy art"
    
    for config in test_configs:
        print(f"Testing {config['name']} configuration...")
        try:
            results = generate_images_with_schedulers(
                prompt=prompt,
                schedulers_to_test=config["schedulers"],
                num_inference_steps=config["steps"],
                height=config["height"],
                width=config["width"],
                output_dir=f"custom_{config['name']}",
                filename_prefix=f"forest_{config['name']}"
            )
            print(f"  {config['name']} completed: {len(results)} images")
        except Exception as e:
            print(f"  Error with {config['name']}: {e}")

if __name__ == "__main__":
    print("Scheduler Testing Examples")
    print("=" * 50)
    
    # Initialize pipeline first
    try:
        print("Initializing pipeline...")
        initialize_pipeline()
        print("Pipeline initialized successfully!\n")
    except Exception as e:
        print(f"Error initializing pipeline: {e}")
        exit(1)
    
    # List available schedulers
    list_available_schedulers()
    
    # Run examples (comment out any you don't want to run)
    
    # Example 1: Test specific schedulers (faster)
    example_test_specific_schedulers()
    
    # Example 2: Custom parameters
    example_custom_parameters()
    
    # Example 3: Quality vs speed comparison
    # example_quality_comparison()
    
    # Example 4: Test all schedulers (this will take a long time!)
    # example_test_all_schedulers()
    
    print("\n=== Examples completed ===")
    print("Check the output directories for generated images!")
