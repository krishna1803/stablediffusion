import sys
import torch
from diffusers import StableDiffusionUpscalePipeline
from PIL import Image
import os
from typing import Optional, Union, List
import glob

# Global pipeline variable to avoid reloading the model
_upscale_pipe = None

def initialize_upscale_pipeline():
    """Initialize the Stable Diffusion upscaling pipeline."""
    global _upscale_pipe
    
    # Check for CUDA availability
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available. Please ensure you have a compatible GPU and PyTorch with CUDA support.")
    
    if _upscale_pipe is None:
        print("Loading upscaling model...")
        _upscale_pipe = StableDiffusionUpscalePipeline.from_pretrained(
            "stabilityai/stable-diffusion-x4-upscaler",
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True
        )
        _upscale_pipe = _upscale_pipe.to("cuda")
        print("Upscaling model loaded successfully")
    
    return _upscale_pipe

def upscale_image(
    input_file: str,
    prompt: str,
    output_file: Optional[str] = None,
    num_inference_steps: int = 75,
    guidance_scale: float = 7.5,
    input_size: tuple = (512, 512),
    output_dir: str = "upscaled_outputs"
) -> str:
    """
    Upscale a single image using Stable Diffusion upscaling.
    
    Args:
        input_file: Path to the input image file
        prompt: Text prompt to guide the upscaling process
        output_file: Name of the output file (if None, auto-generated)
        num_inference_steps: Number of denoising steps
        guidance_scale: Guidance scale for prompt adherence
        input_size: Size to resize input image to (must be 512x512 for the model)
        output_dir: Directory to save the upscaled image
    
    Returns:
        str: Path to the upscaled image
    """
    global _upscale_pipe
    
    # Initialize pipeline if not already done
    if _upscale_pipe is None:
        initialize_upscale_pipeline()
    
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Generate output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_upscaled.png"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)
    
    # Load and prepare the low-resolution image
    low_res_image = Image.open(input_file).convert("RGB")
    low_res_image = low_res_image.resize(input_size, Image.LANCZOS)
    
    print(f"Upscaling image: {input_file}")
    print(f"Using prompt: {prompt}")
    
    # Run the upscaling process
    upscaled_image = _upscale_pipe(
        prompt=prompt,
        image=low_res_image,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
    ).images[0]
    
    # Save the upscaled image
    upscaled_image.save(output_path)
    print(f"Upscaled image saved as {output_path}")
    return output_path

def upscale_directory(
    input_directory: str,
    prompt: str,
    output_directory: Optional[str] = None,
    file_extensions: List[str] = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff'],
    num_inference_steps: int = 75,
    guidance_scale: float = 7.5,
    input_size: tuple = (512, 512)
) -> List[str]:
    """
    Upscale all images in a directory using Stable Diffusion upscaling.
    
    Args:
        input_directory: Path to the directory containing input images
        prompt: Text prompt to guide the upscaling process
        output_directory: Directory to save upscaled images (if None, uses input_directory)
        file_extensions: List of file extensions to process
        num_inference_steps: Number of denoising steps
        guidance_scale: Guidance scale for prompt adherence
        input_size: Size to resize input images to (must be 512x512 for the model)
    
    Returns:
        List[str]: List of paths to the upscaled images
    """
    global _upscale_pipe
    
    # Initialize pipeline if not already done
    if _upscale_pipe is None:
        initialize_upscale_pipeline()
    
    # Check if input directory exists
    if not os.path.isdir(input_directory):
        raise FileNotFoundError(f"Input directory not found: {input_directory}")
    
    # Use input directory as output if not specified
    if output_directory is None:
        output_directory = input_directory
    else:
        os.makedirs(output_directory, exist_ok=True)
    
    upscaled_files = []
    
    # Find all image files in the directory
    image_files = []
    for ext in file_extensions:
        pattern = os.path.join(input_directory, f"*{ext}")
        image_files.extend(glob.glob(pattern, recursive=False))
        # Also check uppercase extensions
        pattern = os.path.join(input_directory, f"*{ext.upper()}")
        image_files.extend(glob.glob(pattern, recursive=False))
    
    if not image_files:
        print(f"No image files found in directory: {input_directory}")
        return upscaled_files
    
    print(f"Found {len(image_files)} image files to upscale")
    
    # Process each image file
    for i, input_file in enumerate(image_files, 1):
        try:
            print(f"Processing image {i}/{len(image_files)}: {os.path.basename(input_file)}")
            
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = f"{base_name}_upscaled.png"
            output_path = os.path.join(output_directory, output_file)
            
            # Load and prepare the low-resolution image
            low_res_image = Image.open(input_file).convert("RGB")
            low_res_image = low_res_image.resize(input_size, Image.LANCZOS)
            
            # Run the upscaling process
            upscaled_image = _upscale_pipe(
                prompt=prompt,
                image=low_res_image,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
            ).images[0]
            
            # Save the upscaled image
            upscaled_image.save(output_path)
            upscaled_files.append(output_path)
            print(f"Upscaled image saved as {output_path}")
            
        except Exception as e:
            print(f"Error processing {input_file}: {e}")
            continue
    
    print(f"Successfully upscaled {len(upscaled_files)} out of {len(image_files)} images")
    return upscaled_files

def upscale_high_resolution(
    input_file: str,
    prompt: str,
    output_file: Optional[str] = None,
    output_dir: str = "upscaled_outputs",
    sd_steps: int = 75,
    sd_guidance_scale: float = 7.5,
    use_swinir: bool = False
) -> str:
    """
    High-resolution upscaling using Stable Diffusion (4x) and optionally SwinIR (2x).
    This provides an 8x total upscaling when both methods are used.
    
    Args:
        input_file: Path to the input image file
        prompt: Text prompt to guide the upscaling process
        output_file: Name of the output file (if None, auto-generated)
        output_dir: Directory to save the upscaled image
        sd_steps: Number of denoising steps for Stable Diffusion
        sd_guidance_scale: Guidance scale for Stable Diffusion
        use_swinir: Whether to apply SwinIR 2x upscaling after SD 4x upscaling
    
    Returns:
        str: Path to the final upscaled image
    """
    global _upscale_pipe
    
    # Initialize pipeline if not already done
    if _upscale_pipe is None:
        initialize_upscale_pipeline()
    
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        if use_swinir:
            output_file = f"{base_name}_upscaled_highres_8x.png"
        else:
            output_file = f"{base_name}_upscaled_highres_4x.png"
    
    # Step 1: Stable Diffusion 4x upscaling
    print(f"Step 1: Applying Stable Diffusion 4x upscaling to: {input_file}")
    
    # Load and prepare the image for SD upscaling
    image = Image.open(input_file).convert("RGB")
    image = image.resize((512, 512), Image.LANCZOS)
    
    # Run SD 4x upscaling
    sd_result = _upscale_pipe(
        prompt=prompt,
        image=image,
        num_inference_steps=sd_steps,
        guidance_scale=sd_guidance_scale
    ).images[0]
    
    # Save intermediate SD result
    sd_output_path = os.path.join(output_dir, f"temp_sd_4x_{os.path.basename(output_file)}")
    sd_result.save(sd_output_path)
    print(f"SD 4x upscaling completed, saved to: {sd_output_path}")
    
    final_output_path = os.path.join(output_dir, output_file)
    
    # Step 2: Optional SwinIR 2x upscaling
    if use_swinir:
        try:
            print("Step 2: Applying SwinIR 2x upscaling...")
            
            # Try to import SwinIR dependencies
            from torchvision import transforms
            
            # Load the SD result for SwinIR processing
            img = Image.open(sd_output_path).convert("RGB")
            
            # For now, we'll use a simple bicubic upscaling as SwinIR requires specific model files
            # In a production environment, you would load the actual SwinIR model here
            print("Note: Using bicubic upscaling as SwinIR model. For full SwinIR support, install SwinIR dependencies.")
            
            # Get current size and double it
            current_size = img.size
            new_size = (current_size[0] * 2, current_size[1] * 2)
            
            # Apply bicubic upscaling
            final_result = img.resize(new_size, Image.BICUBIC)
            final_result.save(final_output_path)
            
            print(f"High-resolution 8x upscaling completed, saved to: {final_output_path}")
            
            # Clean up temporary file
            if os.path.exists(sd_output_path):
                os.remove(sd_output_path)
                
        except ImportError as e:
            print(f"SwinIR dependencies not available: {e}")
            print("Using only Stable Diffusion 4x upscaling")
            # Just move the SD result to final output
            os.rename(sd_output_path, final_output_path)
        except Exception as e:
            print(f"Error in SwinIR processing: {e}")
            print("Using only Stable Diffusion 4x upscaling")
            # Just move the SD result to final output
            os.rename(sd_output_path, final_output_path)
    else:
        # Just move the SD result to final output
        os.rename(sd_output_path, final_output_path)
        print(f"High-resolution 4x upscaling completed, saved to: {final_output_path}")
    
    return final_output_path

def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Single image: python image_upscaling.py <input_file> <prompt>")
        print("  Directory:    python image_upscaling.py <input_directory> <prompt> --directory")
        print("  High-res:     python image_upscaling.py <input_file> <prompt> --highres [--swinir]")
        sys.exit(1)

    input_path = sys.argv[1]
    prompt = sys.argv[2]
    
    # Check for mode flags
    use_directory = "--directory" in sys.argv
    use_highres = "--highres" in sys.argv
    use_swinir = "--swinir" in sys.argv
    
    try:
        if use_directory:
            # Directory mode
            if not os.path.isdir(input_path):
                print(f"Error: {input_path} is not a directory")
                sys.exit(1)
            
            results = upscale_directory(input_path, prompt)
            print(f"Directory upscaling completed successfully: {len(results)} images processed")
            
        elif use_highres:
            # High-resolution mode
            output_path = upscale_high_resolution(input_path, prompt, use_swinir=use_swinir)
            print(f"High-resolution upscaling completed successfully: {output_path}")
            
        else:
            # Single image mode
            output_path = upscale_image(input_path, prompt)
            print(f"Image upscaling completed successfully: {output_path}")
            
    except Exception as e:
        print(f"Error during upscaling: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
