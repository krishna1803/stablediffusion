import torch
from diffusers import StableDiffusion3Pipeline, StableDiffusionPipeline
import sys
import os
from typing import Optional

# Global pipeline variable to avoid reloading the model
_pipe = None
_current_model_id = None

def initialize_pipeline():
    """Initialize the appropriate Stable Diffusion pipeline based on GPU memory."""
    global _pipe, _current_model_id
    
    # Check for CUDA availability
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available. Please ensure you have a compatible GPU and PyTorch with CUDA support.")
    
    # Get GPU memory in GB
    gpu_memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"Detected GPU memory: {gpu_memory_gb:.1f} GB")
    
    # Select model and pipeline based on GPU memory
    if gpu_memory_gb <= 24:
        print("Using Stable Diffusion 2.1 (GPU memory <= 24 GB)")
        model_id = "stabilityai/stable-diffusion-2-1"
        _pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    elif gpu_memory_gb <= 48:
        print("Using Stable Diffusion 3.5 Medium (24 GB < GPU memory <= 48 GB)")
        model_id = "stabilityai/stable-diffusion-3.5-medium"
        _pipe = StableDiffusion3Pipeline.from_pretrained(model_id, torch_dtype=torch.bfloat16)
    else:
        print("Using Stable Diffusion 3.5 Large (GPU memory > 48 GB)")
        model_id = "stabilityai/stable-diffusion-3.5-large"
        _pipe = StableDiffusion3Pipeline.from_pretrained(model_id, torch_dtype=torch.bfloat16)
    
    _pipe = _pipe.to("cuda")
    _current_model_id = model_id
    return _pipe

def generate_image(
    prompt: str,
    output_file: str,
    negative_prompt: Optional[str] = "blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face",
    num_inference_steps: int = 50,
    guidance_scale: float = 7.0,
    height: int = 1024,
    width: int = 1024,
    output_dir: str = "final_outputs",
    upscale: bool = False,
    upscale_prompt: Optional[str] = None
) -> str:
    """
    Generate an image using Stable Diffusion.
    
    Args:
        prompt: Text prompt for image generation
        output_file: Name of the output file (with extension)
        negative_prompt: Negative prompt to avoid unwanted features
        num_inference_steps: Number of denoising steps
        guidance_scale: Guidance scale for prompt adherence
        height: Image height in pixels
        width: Image width in pixels
        output_dir: Directory to save the output image
        upscale: Whether to upscale the generated image
        upscale_prompt: Prompt for upscaling (if None, uses the original prompt)
    
    Returns:
        str: Path to the saved image (upscaled if requested)
    """
    global _pipe
    
    # Initialize pipeline if not already done
    if _pipe is None:
        initialize_pipeline()
    
    # Ensure output folder exists
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)
    
    # Generate image
    image = _pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        height=height,
        width=width
    ).images[0]
    
    # Save image
    image.save(output_path)
    print(f"Image saved to {output_path}")
    
    # Upscale if requested
    if upscale:
        try:
            from image_upscaling import upscale_image
            upscale_prompt_text = upscale_prompt if upscale_prompt else prompt
            
            # Generate upscaled filename
            base_name = os.path.splitext(output_file)[0]
            upscaled_filename = f"{base_name}_upscaled.png"
            
            upscaled_path = upscale_image(
                input_file=output_path,
                prompt=upscale_prompt_text,
                output_file=upscaled_filename,
                output_dir=output_dir
            )
            print(f"Upscaled image saved to {upscaled_path}")
            return upscaled_path
        except ImportError:
            print("Warning: Could not import upscaling module. Returning original image.")
        except Exception as e:
            print(f"Warning: Upscaling failed: {e}. Returning original image.")
    
    return output_path

def main():
    """Main function for command-line usage."""
    # Get the prompt and output file name from command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python imagegeneration_final.py <prompt> <output_file>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        output_path = generate_image(prompt, output_file)
        print(f"Image generation completed successfully: {output_path}")
    except Exception as e:
        print(f"Error generating image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
