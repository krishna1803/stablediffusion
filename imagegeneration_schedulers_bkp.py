import torch
from diffusers import (
    StableDiffusionPipeline,
    DDIMScheduler,
    DPMSolverMultistepScheduler,
    EulerAncestralDiscreteScheduler,
    HeunDiscreteScheduler,
    LMSDiscreteScheduler,
    PNDMScheduler,
) 
    
import os

# Define prompt details
prompt = (
    "Captured in a cinematic shot, a pristine white dual-tone right-hand drive Tata Motors Punch EV 2024 model stands proudly in front of a vibrant Kerala school with a backdrop of lush green mountains and towering coconut trees."
    "A Kerala female teacher, in her mid-thirties simling, adorned in a traditional Kerala Kasavu saree with intricate golden borders, stands by the side of the car.She holds a stack of books in her hands, conveying the essence of knowledge and learning." 
    "The image is bathed in natural light,with a muted color palette,creating a serene and educational atmosphere."
)
negative_prompt = (
    "blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face"
)

# Scheduler name to class mapping
schedulers = {
    "DDIM": DDIMScheduler,
    "DPM": DPMSolverMultistepScheduler,
    "EulerA": EulerAncestralDiscreteScheduler,
    "Heun": HeunDiscreteScheduler,
    "LMS": LMSDiscreteScheduler,
    "PNDM": PNDMScheduler,
}

# Set base model once
base_pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1", torch_dtype=torch.bfloat16
)

# Ensure output folder
os.makedirs("outputs", exist_ok=True)

# Loop through each scheduler
for name, SchedulerClass in schedulers.items():
    print(f"Generating image with scheduler: {name}")

    # Replace scheduler
    scheduler = SchedulerClass.from_config(base_pipe.scheduler.config)
    pipe = base_pipe.to("cuda")
    pipe.scheduler = scheduler

    # Run inference
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=100,
        guidance_scale=8.0,
        height=1024,
        width=1024
    ).images[0]

    # Save image
    filename = f"outputs/tatanano_sd2.1_{name.lower()}_100_steps.png"
    image.save(filename)
    print(f"Saved: {filename}")
