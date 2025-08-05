from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import subprocess
import os
import uuid

app = FastAPI()

@app.post("/generate-image/")
async def generate_image(
    prompt: str = Form(...),
    negative_prompt: str = Form("blurry, distorted, low quality, extra limbs, poorly drawn, cartoon, surreal, low resolution, unrealistic lighting, bad proportions, overexposed, deformed"),
    num_inference_steps: int = Form(70),
    guidance_scale: float = Form(9.0),
    height: int = Form(1024),
    width: int = Form(1024),
    model_name: str = Form("stabilityai/stable-diffusion-3.5-large"),
    output_dir: str = Form("final_outputs")
):
    output_file = f"{uuid.uuid4().hex}.png"
    cmd = [
        "python", "imagegeneration_final.py", prompt, output_file, negative_prompt,
        str(num_inference_steps), str(guidance_scale), str(height), str(width), model_name, output_dir
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return JSONResponse(status_code=500, content={"error": result.stderr})
    output_path = os.path.join(output_dir, output_file)
    return FileResponse(output_path, media_type="image/png")

@app.post("/upscale-image/")
async def upscale_image(
    file: UploadFile = File(...),
    prompt: str = Form("A photorealistic upscaled image")
):
    temp_input = f"temp_{uuid.uuid4().hex}.png"
    temp_output = temp_input.rsplit('.', 1)[0] + "_upscaled.png"
    with open(temp_input, "wb") as f:
        f.write(await file.read())
    cmd = ["python", "image_upscaling.py", temp_input, prompt]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        os.remove(temp_input)
        return JSONResponse(status_code=500, content={"error": result.stderr})
    response = FileResponse(temp_output, media_type="image/png")
    os.remove(temp_input)
    # Optionally, remove the upscaled file after sending
    # os.remove(temp_output)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
