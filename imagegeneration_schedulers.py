import torch
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusion3Pipeline,
    DDIMScheduler,
    DDPMScheduler,
    DEISMultistepScheduler,
    DPMSolverMultistepScheduler,
    DPMSolverSinglestepScheduler,
    DPMSolverSDEScheduler,
    EDMDPMSolverMultistepScheduler,
    EDMEulerScheduler,
    EulerAncestralDiscreteScheduler,
    EulerDiscreteScheduler,
    HeunDiscreteScheduler,
    IPNDMScheduler,
    KDPM2AncestralDiscreteScheduler,
    KDPM2DiscreteScheduler,
    LCMScheduler,
    LMSDiscreteScheduler,
    PNDMScheduler
)
import os
import sys
from typing import Optional, List, Dict, Any

# Global pipeline variable to avoid reloading the model
_pipe = None
_current_model_id = None

# Scheduler name to class mapping
SCHEDULERS = {
    "DDIM": DDIMScheduler,
    "DDPM": DDPMScheduler,
    "DEISMultistep": DEISMultistepScheduler,
    "DPMSolverMultistep": DPMSolverMultistepScheduler,
    "DPMSolverSinglestep": DPMSolverSinglestepScheduler,
    "DPMSolverSDE": DPMSolverSDEScheduler,
    "EDMDPMSolverMultistep": EDMDPMSolverMultistepScheduler,
    "EDMEuler": EDMEulerScheduler,
    "EulerAncestral": EulerAncestralDiscreteScheduler,
    "EulerDiscrete": EulerDiscreteScheduler,
    "HeunDiscrete": HeunDiscreteScheduler,
    "IPNDM": IPNDMScheduler,
    "KDPM2Ancestral": KDPM2AncestralDiscreteScheduler,
    "KDPM2": KDPM2DiscreteScheduler,
    "LCM": LCMScheduler,
    "LMS": LMSDiscreteScheduler,
    "PNDM": PNDMScheduler,
}

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

def generate_images_with_schedulers(
    prompt: str,
    negative_prompt: Optional[str] = "blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face",
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5,
    height: int = 768,
    width: int = 768,
    output_dir: str = "scheduler_outputs",
    schedulers_to_test: Optional[List[str]] = None,
    filename_prefix: str = "scheduler_test"
) -> Dict[str, str]:
    """
    Generate images using different schedulers.
    
    Args:
        prompt: Text prompt for image generation
        negative_prompt: Negative prompt to avoid unwanted features
        num_inference_steps: Number of denoising steps
        guidance_scale: Guidance scale for prompt adherence
        height: Image height in pixels
        width: Image width in pixels
        output_dir: Directory to save the output images
        schedulers_to_test: List of scheduler names to test (if None, tests all)
        filename_prefix: Prefix for output filenames
    
    Returns:
        Dict[str, str]: Dictionary mapping scheduler names to output file paths
    """
    global _pipe
    
    # Initialize pipeline if not already done
    if _pipe is None:
        initialize_pipeline()
    
    # Use all schedulers if none specified
    if schedulers_to_test is None:
        schedulers_to_test = list(SCHEDULERS.keys())
    
    # Ensure output folder exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Store the original scheduler
    original_scheduler = _pipe.scheduler
    results = {}
    
    print(f"Testing {len(schedulers_to_test)} schedulers...")
    
    # Loop through each scheduler
    for scheduler_name in schedulers_to_test:
        if scheduler_name not in SCHEDULERS:
            print(f"Warning: Unknown scheduler '{scheduler_name}', skipping...")
            continue
            
        print(f"Generating image with scheduler: {scheduler_name}")
        
        try:
            # Replace scheduler
            SchedulerClass = SCHEDULERS[scheduler_name]
            scheduler = SchedulerClass.from_config(_pipe.scheduler.config)
            _pipe.scheduler = scheduler
            
            # Run inference
            image = _pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                height=height,
                width=width
            ).images[0]
            
            # Generate filename based on scheduler
            sanitized_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            sanitized_prompt = sanitized_prompt.replace(' ', '_').lower()
            filename = f"{filename_prefix}_{sanitized_prompt}_{scheduler_name.lower()}_{num_inference_steps}steps.png"
            full_path = os.path.join(output_dir, filename)
            
            # Save image
            image.save(full_path)
            results[scheduler_name] = full_path
            print(f"Saved: {full_path}")
            
        except Exception as e:
            print(f"Error with scheduler {scheduler_name}: {e}")
            continue
    
    # Restore original scheduler
    _pipe.scheduler = original_scheduler
    
    return results

def generate_image_with_scheduler(
    prompt: str,
    scheduler_name: str,
    negative_prompt: Optional[str] = "blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face",
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5,
    height: int = 768,
    width: int = 768,
    output_dir: str = "scheduler_outputs",
    filename_prefix: str = "single_scheduler"
) -> str:
    """
    Generate a single image using a specific scheduler.
    
    Args:
        prompt: Text prompt for image generation
        scheduler_name: Name of the scheduler to use
        negative_prompt: Negative prompt to avoid unwanted features
        num_inference_steps: Number of denoising steps
        guidance_scale: Guidance scale for prompt adherence
        height: Image height in pixels
        width: Image width in pixels
        output_dir: Directory to save the output image
        filename_prefix: Prefix for output filename
    
    Returns:
        str: Path to the generated image
    """
    global _pipe
    
    # Initialize pipeline if not already done
    if _pipe is None:
        initialize_pipeline()
    
    # Check if scheduler exists
    if scheduler_name not in SCHEDULERS:
        raise ValueError(f"Unknown scheduler '{scheduler_name}'. Available schedulers: {list(SCHEDULERS.keys())}")
    
    # Ensure output folder exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Store the original scheduler
    original_scheduler = _pipe.scheduler
    
    try:
        print(f"Generating image with scheduler: {scheduler_name}")
        
        # Replace scheduler
        SchedulerClass = SCHEDULERS[scheduler_name]
        scheduler = SchedulerClass.from_config(_pipe.scheduler.config)
        _pipe.scheduler = scheduler
        
        # Run inference
        image = _pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            height=height,
            width=width
        ).images[0]
        
        # Generate filename
        sanitized_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        sanitized_prompt = sanitized_prompt.replace(' ', '_').lower()
        filename = f"{filename_prefix}_{sanitized_prompt}_{scheduler_name.lower()}_{num_inference_steps}steps.png"
        full_path = os.path.join(output_dir, filename)
        
        # Save image
        image.save(full_path)
        print(f"Saved: {full_path}")
        
        return full_path
        
    except Exception as e:
        raise RuntimeError(f"Error generating image with scheduler {scheduler_name}: {e}")
    finally:
        # Restore original scheduler
        _pipe.scheduler = original_scheduler

def main():
    """Main function for command-line usage."""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Test all schedulers: python imagegeneration_schedulers.py \"<prompt>\"")
        print("  Test specific schedulers: python imagegeneration_schedulers.py \"<prompt>\" \"scheduler1,scheduler2,scheduler3\"")
        print("  Single scheduler: python imagegeneration_schedulers.py \"<prompt>\" --single <scheduler_name>")
        print("  List schedulers: python imagegeneration_schedulers.py --list")
        print(f"\nAvailable schedulers: {', '.join(SCHEDULERS.keys())}")
        sys.exit(1)
    
    # Handle --list option
    if sys.argv[1] == "--list":
        print("Available schedulers:")
        for i, scheduler in enumerate(SCHEDULERS.keys(), 1):
            print(f"  {i:2d}. {scheduler}")
        print(f"\nTotal: {len(SCHEDULERS)} schedulers")
        sys.exit(0)
    
    # Get prompt from command line
    prompt = sys.argv[1]
    
    # Handle single scheduler mode
    if len(sys.argv) > 2 and sys.argv[2] == "--single":
        if len(sys.argv) < 4:
            print("Error: Please specify a scheduler name for --single mode")
            print(f"Available schedulers: {', '.join(SCHEDULERS.keys())}")
            sys.exit(1)
        
        scheduler_name = sys.argv[3]
        
        try:
            output_path = generate_image_with_scheduler(
                prompt=prompt,
                scheduler_name=scheduler_name,
                filename_prefix="custom"
            )
            print(f"\nImage generation completed successfully!")
            print(f"Generated image: {output_path}")
            
        except Exception as e:
            print(f"Error generating image: {e}")
            sys.exit(1)
        
        return
    
    # Handle multiple schedulers mode
    schedulers_to_test = None
    if len(sys.argv) > 2:
        schedulers_input = sys.argv[2].split(",")
        schedulers_to_test = [s.strip() for s in schedulers_input]
        
        # Validate scheduler names
        invalid_schedulers = [s for s in schedulers_to_test if s not in SCHEDULERS]
        if invalid_schedulers:
            print(f"Error: Invalid scheduler(s): {', '.join(invalid_schedulers)}")
            print(f"Available schedulers: {', '.join(SCHEDULERS.keys())}")
            sys.exit(1)
        
        print(f"Testing specific schedulers: {schedulers_to_test}")
    else:
        print(f"Testing all available schedulers: {list(SCHEDULERS.keys())}")
    
    try:
        results = generate_images_with_schedulers(
            prompt=prompt,
            schedulers_to_test=schedulers_to_test,
            filename_prefix="comparison"
        )
        
        print(f"\nGeneration completed successfully!")
        print(f"Generated {len(results)} images:")
        for scheduler, path in results.items():
            print(f"  {scheduler}: {path}")
            
    except Exception as e:
        print(f"Error generating images: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
