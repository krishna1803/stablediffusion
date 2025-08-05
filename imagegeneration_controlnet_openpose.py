from diffusers import ControlNetModel, AutoPipelineForText2Image
from diffusers.utils import load_image
import torch
 
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_OpenPose",
    torch_dtype=torch.float16,
    variant="fp16",
).to("cuda")
 
original_image = load_image(
"tatanano_advanced_250steps_photorealistic_2.png"
)

from PIL import Image
 
def image_grid(imgs, rows, cols, resize=256):
    assert len(imgs) == rows * cols
 
    if resize is not None:
        imgs = [img.resize((resize, resize)) for img in imgs]
    w, h = imgs[0].size
    grid_w, grid_h = cols * w, rows * h
    grid = Image.new("RGB", size=(grid_w, grid_h))
 
    for i, img in enumerate(imgs):
        x = i % cols * w
        y = i // cols * h
        grid.paste(img, box=(x, y))
    return grid

from controlnet_aux import OpenposeDetector
 
model = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
pose_image = model(original_image)
 
image_grid([original_image,pose_image], 1, 2)


controlnet_pipe = AutoPipelineForText2Image.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16,
    variant="fp16",
).to("cuda")

prompt = "A highly detailed photorealistic photo of a Tata Nano car parked outside a school in Kerala,India "\
        "and a beautiful school teacher in colorful saree standing near the car,sharp focus,8k resolution,hyperrealism,photorealistic"
neg_prompt = "worst quality, low quality, lowres, monochrome, greyscale, " \
             "multiple views, comic, sketch, bad anatomy, deformed, disfigured, " \
             "watermark, multiple_views, mutation hands, watermark, bad facial"
 
image = controlnet_pipe(
    prompt,
    negative_prompt=neg_prompt,
    num_images_per_prompt = 1,
    image=pose_image,
).images[0]
#image_grid(image, 1, 1)
image.save("tatanano_advanced_250steps_photorealistic_2_controlnet.png")