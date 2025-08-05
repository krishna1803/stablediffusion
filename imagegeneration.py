import torch
from diffusers import StableDiffusion3Pipeline

pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3.5-large", torch_dtype=torch.bfloat16)
pipe = pipe.to("cuda")

image = pipe(
    "Draw a picture of a Tata Nano car. A school teacher in saree is standing near the car. Generate the car in 4k resolution",
    num_inference_steps=50,
    guidance_scale=3.5,
).images[0]
image.save("tatanano_50.png")
