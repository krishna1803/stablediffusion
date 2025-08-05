import torch
from diffusers import StableDiffusion3Pipeline

pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3.5-large", torch_dtype=torch.bfloat16)
pipe = pipe.to("cuda")

image = pipe(
    #prompt="A highly detailed photorealistic photo of a Tata Nano car parked outside a school in Kerala,India \
    #    and a beautiful school teacher in colorful saree standing near the car,sharp focus,8k resolution,hyperrealism,photorealistic",
    prompt = "A yellow Tata Nano car, a compact Indian hatchback, parked in front of a rural school building in Kerala. "\
    "An elegant young Indian school teacher wearing a colorful saree stands beside the car, smiling with smooth white teeth. "\
    "The scene is bathed in warm sunlight, photorealistic, ultra detailed, 8k high resolution, cinematic composition, sharp focus" ,   
    negative_prompt="blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face",
    num_inference_steps=60,
    guidance_scale=5.0,
    height=1024,
    width=1024
).images[0]
image.save("tatanano_advanced_250steps_photorealistic_7.png")
