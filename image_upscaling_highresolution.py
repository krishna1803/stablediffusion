import torch
from PIL import Image
from diffusers import StableDiffusionUpscalePipeline
from torchvision import transforms
from swinir.models import define_model
import os

def upscale_with_stable_diffusion(input_path, prompt, output_path):
    # Load SD Upscaler
    sd_pipe = StableDiffusionUpscalePipeline.from_pretrained(
        "stabilityai/stable-diffusion-x4-upscaler",
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True
    ).to("cuda")

    # Load base image and resize
    image = Image.open(input_path).convert("RGB")
    image = image.resize((512, 512), Image.LANCZOS)

    # Run SD 4x upscaling
    result = sd_pipe(
        prompt=prompt,
        image=image,
        num_inference_steps=75,
        guidance_scale=7.5
    ).images[0]
    result.save(output_path)
    print(f"[✓] Saved 4x SD output to: {output_path}")
    return output_path

def upscale_with_swinir(input_path, output_path):
    # Load and preprocess
    img = Image.open(input_path).convert("RGB")
    img_tensor = transforms.ToTensor()(img).unsqueeze(0).to("cuda")

    # Define SwinIR model
    model = define_model(
        scale=2,
        model_type='swinir',
        task='real_sr',
        pretrained=True
    ).to("cuda")
    model.eval()

    # Inference
    with torch.no_grad():
        output_tensor = model(img_tensor)

    # Convert and save
    output_img = transforms.ToPILImage()(output_tensor.squeeze(0).clamp(0, 1).cpu())
    output_img.save(output_path)
    print(f"[✓] Saved SwinIR output to: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python upscale_highresolution.py <input_image.png> <prompt>")
        exit(1)

    input_image = sys.argv[1]
    prompt = sys.argv[2]

    os.makedirs("upscaled_outputs", exist_ok=True)

    # Step 1: SD x4
    sd_out = f"upscaled_outputs/{input_image.rsplit('.', 1)[0]}_upscaled_sdx.png"
    upscale_with_stable_diffusion(input_image, prompt, sd_out)

    # Step 2: SwinIR x2
    swinir_out = f"upscaled_outputs/{input_image.rsplit('.', 1)[0]}_upscaled_swinsr.png"
    upscale_with_swinir(sd_out, swinir_out)
