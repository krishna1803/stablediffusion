import torch
from diffusers import StableDiffusion3Pipeline

pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3.5-large", torch_dtype=torch.bfloat16)
pipe = pipe.to("cuda")

image = pipe(
    #prompt="A highly detailed photorealistic photo of a Tata Nano car parked outside a school in Kerala,India \
    #    and a beautiful school teacher in colorful saree standing near the car,sharp focus,8k resolution,hyperrealism,photorealistic",
    prompt = "Captured in a cinematic shot, a pristine white dual-tone right-hand drive Tata Motors Punch EV 2024 model stands proudly in front of a vibrant Kerala school with a backdrop of lush green mountains and towering coconut trees."
    "A Kerala female teacher, in her mid-thirties, adorned in a traditional Kerala Kasavu saree with intricate golden borders, stands by the side of the car. ",
    prompt_2 = "The Kerala female teacher's warm smile and friendly face radiate kindness, while she holds a stack of books in her hands, conveying the essence of knowledge and learning." 
    "The image is bathed in natural light,with a muted color palette,creating a serene and educational atmosphere." ,
    prompt_3= "The 50mm lens captures a detailed view of the Tata Motors Punch EV 2024 model car in its entirity and the Kerala female teacher, while the background enhances the overall aesthetic, focusing the viewer's attention on the primary subjects." ,
    negative_prompt="blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face",
    negative_prompt_2="blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face",
    negative_prompt_3="blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face",
    num_inference_steps=60,
    guidance_scale=5.0,
    height=1024,
    width=1024
).images[0]
image.save("tml_advanced_250steps_photorealistic_6.png")
