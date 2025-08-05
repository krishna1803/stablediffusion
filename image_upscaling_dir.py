import sys
import os
import torch
from diffusers import StableDiffusionUpscalePipeline
from PIL import Image

# Load the upscaler model from StabilityAI
pipe = StableDiffusionUpscalePipeline.from_pretrained(
    "stabilityai/stable-diffusion-x4-upscaler",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
)
pipe = pipe.to("cuda")

# Get the input directory and prompt from command-line arguments
if len(sys.argv) < 3:
    print("Usage: python image_upscaling_dir.py <input_directory> <prompt>")
    sys.exit(1)

input_directory = sys.argv[1]
prompt = sys.argv[2]

# Check if the input directory exists
if not os.path.isdir(input_directory):
    print(f"Error: Directory '{input_directory}' does not exist.")
    sys.exit(1)

# Process all .png files in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith(".png"):
        input_file = os.path.join(input_directory, file_name)
        output_file = os.path.join(input_directory, f"{file_name.rsplit('.', 1)[0]}_upscaled.png")

        # Load and prepare the low-resolution image
        low_res_image = Image.open(input_file).convert("RGB")
        low_res_image = low_res_image.resize((512, 512), Image.LANCZOS)  # Must be 512x512 input

        # Run the upscaling process
        upscaled_image = pipe(
            prompt=prompt,
            image=low_res_image,
            num_inference_steps=75,
            guidance_scale=7.5,
        ).images[0]

        # Save the upscaled image
        upscaled_image.save(output_file)
        print(f"Upscaled image saved as {output_file}")
