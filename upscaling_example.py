"""
Example of using the upscaling function directly from image_upscaling.py

This script demonstrates how to:
1. Use the upscaling function directly in Python code
2. Upscale an existing image with custom parameters
"""

from image_upscaling import upscale_image, initialize_upscale_pipeline
import os

def example_direct_upscaling():
    """Example of using the upscaling function directly."""
    
    # You can optionally initialize the pipeline first (it will be done automatically if not)
    print("Initializing upscaling pipeline...")
    try:
        initialize_upscale_pipeline()
        print("Pipeline initialized successfully!")
    except Exception as e:
        print(f"Error initializing pipeline: {e}")
        return
    
    # Example 1: Basic upscaling
    input_image = "final_outputs/test_image.png"  # Replace with your actual image path
    
    if os.path.exists(input_image):
        print(f"\nUpscaling image: {input_image}")
        
        try:
            upscaled_path = upscale_image(
                input_file=input_image,
                prompt="enhance details, high quality, photorealistic",
                num_inference_steps=50,
                guidance_scale=7.5
            )
            print(f"Upscaled image saved to: {upscaled_path}")
            
        except Exception as e:
            print(f"Error during upscaling: {e}")
    else:
        print(f"Input image not found: {input_image}")
        print("Please generate an image first or provide a valid image path.")
    
    # Example 2: Custom parameters
    print("\nExample with custom parameters:")
    
    # You can customize various parameters
    custom_params = {
        "num_inference_steps": 75,  # More steps for better quality
        "guidance_scale": 8.0,      # Higher guidance for stronger prompt adherence
        "output_dir": "custom_upscaled",  # Custom output directory
        "output_file": "custom_upscaled_image.png"  # Custom filename
    }
    
    if os.path.exists(input_image):
        try:
            upscaled_path = upscale_image(
                input_file=input_image,
                prompt="ultra high resolution, sharp details, professional photography",
                **custom_params
            )
            print(f"Custom upscaled image saved to: {upscaled_path}")
            
        except Exception as e:
            print(f"Error during custom upscaling: {e}")

def example_from_imagegeneration():
    """Example of generating and then upscaling an image."""
    
    try:
        from imagegeneration_final import generate_image
        
        print("Generating a new image...")
        
        # Generate an image
        generated_path = generate_image(
            prompt="a beautiful landscape with mountains and a lake",
            output_file="landscape_test.png",
            num_inference_steps=30,
            height=512,
            width=512
        )
        
        print(f"Generated image: {generated_path}")
        
        # Now upscale it
        print("Upscaling the generated image...")
        
        upscaled_path = upscale_image(
            input_file=generated_path,
            prompt="enhance landscape details, photorealistic, high resolution",
            num_inference_steps=60,
            guidance_scale=7.5
        )
        
        print(f"Upscaled image: {upscaled_path}")
        
    except ImportError as e:
        print(f"Could not import imagegeneration_final: {e}")
    except Exception as e:
        print(f"Error during generation/upscaling: {e}")

if __name__ == "__main__":
    print("=== Upscaling Examples ===")
    
    # Example 1: Direct upscaling
    print("\n1. Direct upscaling example:")
    example_direct_upscaling()
    
    # Example 2: Generate and upscale
    print("\n2. Generate and upscale example:")
    example_from_imagegeneration()
    
    print("\n=== Examples completed ===")
