import torch
from diffusers import StableDiffusion3Pipeline
import sys
import os

pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3.5-large", torch_dtype=torch.bfloat16)
pipe = pipe.to("cuda")

# Get the prompt and output file name from command-line arguments
if len(sys.argv) < 3:
    print("Usage: python imagegeneration_final.py <prompt> <output_file>")
    sys.exit(1)

prompt = sys.argv[1]
output_file = sys.argv[2]

# Ensure output folder exists
os.makedirs("final_outputs", exist_ok=True)
output_path = os.path.join("final_outputs", output_file)

image = pipe(
    prompt=prompt,
    negative_prompt="blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face",
    num_inference_steps=50,
    guidance_scale=7.0,
    height=1024,
    width=1024
).images[0]
image.save(output_path)
print(f"Image saved to {output_path}")
