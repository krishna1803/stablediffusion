import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

# Load pipeline with DPM++ scheduler for better coherence
pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1",
    torch_dtype=torch.bfloat16
)

pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cuda")

# Improved prompt for structure and recognizability
prompt = (
    "A yellow Tata Nano car, a compact Indian hatchback, parked in front of a rural school building in Kerala. "
    "An elegant Indian school teacher wearing a colorful saree stands beside the car, smiling. "
    "The scene is bathed in warm sunlight, photorealistic, ultra detailed, 8k, cinematic composition, sharp focus"
)

# Cleaner and more controlled negative prompt
negative_prompt = (
    "blurry, low quality, bad anatomy, distorted face, extra limbs, malformed hands, poor composition"
)

# Image generation
image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=60,   # 50–70 is optimal for quality
    guidance_scale=8.0,       # higher adherence to prompt
    height=1024,
    width=1024
).images[0]

# Save image
image.save("tatanano_sd35_high_quality.png")
print("Image saved as tatanano_sd35_DPIM_high_quality.png")
