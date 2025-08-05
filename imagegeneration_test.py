import torch
from diffusers import StableDiffusion3Pipeline

pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3.5-large", torch_dtype=torch.bfloat16)
pipe = pipe.to("cuda")

image = pipe(
    prompt="photo of white cat, sitting outside restaurant, color, wearing dress,rim lighting, studio lighting, looking at the camera, up close, perfect eyes",
    negative_prompt="blurry, low quality, ugly, bad anatomy, deformed hands, extra limbs, poorly drawn face",
    num_inference_steps=150,
    guidance_scale=5.0,
    height=1024,
    width=1024
).images[0]
image.save("white_cat_150steps.png")
