from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import os
import uuid
from imagegeneration_final import generate_image, initialize_pipeline
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI(title="Stable Diffusion Image Generation API", version="1.0.0")

class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt for image generation")
    negative_prompt: Optional[str] = Field(
        "blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face",
        description="Negative prompt to avoid unwanted features"
    )
    num_inference_steps: int = Field(50, ge=1, le=100, description="Number of denoising steps")
    guidance_scale: float = Field(7.0, ge=1.0, le=20.0, description="Guidance scale for prompt adherence")
    height: int = Field(1024, ge=256, le=2048, description="Image height in pixels")
    width: int = Field(1024, ge=256, le=2048, description="Image width in pixels")
    output_dir: str = Field("final_outputs", description="Directory to save the output image")
    upscale: bool = Field(False, description="Whether to upscale the generated image")
    upscale_prompt: Optional[str] = Field(None, description="Prompt for upscaling (if None, uses the original prompt)")

class ImageGenerationResponse(BaseModel):
    message: str
    output_path: str
    filename: str

class UpscaleRequest(BaseModel):
    input_file: str = Field(..., description="Path to the input image file (relative to output_dir)")
    prompt: str = Field(..., description="Text prompt to guide the upscaling process")
    output_file: Optional[str] = Field(None, description="Name of the output file (if None, auto-generated)")
    num_inference_steps: int = Field(75, ge=1, le=100, description="Number of denoising steps")
    guidance_scale: float = Field(7.5, ge=1.0, le=20.0, description="Guidance scale for prompt adherence")
    output_dir: str = Field("upscaled_outputs", description="Directory containing input and output images")

class UpscaleDirectoryRequest(BaseModel):
    input_directory: str = Field(..., description="Path to the directory containing input images")
    prompt: str = Field(..., description="Text prompt to guide the upscaling process")
    output_directory: Optional[str] = Field(None, description="Directory to save upscaled images (if None, uses input_directory)")
    file_extensions: List[str] = Field(['.png', '.jpg', '.jpeg', '.bmp', '.tiff'], description="List of file extensions to process")
    num_inference_steps: int = Field(75, ge=1, le=100, description="Number of denoising steps")
    guidance_scale: float = Field(7.5, ge=1.0, le=20.0, description="Guidance scale for prompt adherence")

class UpscaleHighResolutionRequest(BaseModel):
    input_file: str = Field(..., description="Path to the input image file (relative to output_dir)")
    prompt: str = Field(..., description="Text prompt to guide the upscaling process")
    output_file: Optional[str] = Field(None, description="Name of the output file (if None, auto-generated)")
    output_dir: str = Field("upscaled_outputs", description="Directory to save the upscaled image")
    sd_steps: int = Field(75, ge=1, le=100, description="Number of denoising steps for Stable Diffusion")
    sd_guidance_scale: float = Field(7.5, ge=1.0, le=20.0, description="Guidance scale for Stable Diffusion")
    use_swinir: bool = Field(False, description="Whether to apply SwinIR 2x upscaling after SD 4x upscaling")

class UpscaleResponse(BaseModel):
    message: str
    output_path: str
    filename: str

class UpscaleDirectoryResponse(BaseModel):
    message: str
    output_paths: List[str]
    total_processed: int
    successful_upscales: int

class SchedulerTestRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt for image generation")
    negative_prompt: Optional[str] = Field(
        "blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face",
        description="Negative prompt to avoid unwanted features"
    )
    schedulers_to_test: Optional[List[str]] = Field(None, description="List of scheduler names to test (if None, tests all)")
    num_inference_steps: int = Field(50, ge=1, le=100, description="Number of denoising steps")
    guidance_scale: float = Field(7.5, ge=1.0, le=20.0, description="Guidance scale for prompt adherence")
    height: int = Field(768, ge=256, le=2048, description="Image height in pixels")
    width: int = Field(768, ge=256, le=2048, description="Image width in pixels")
    output_dir: str = Field("scheduler_outputs", description="Directory to save the output images")
    filename_prefix: str = Field("scheduler_test", description="Prefix for output filenames")

class SchedulerTestResponse(BaseModel):
    message: str
    results: Dict[str, str]
    total_generated: int
    available_schedulers: List[str]

class SingleSchedulerRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt for image generation")
    scheduler_name: str = Field(..., description="Name of the scheduler to use")
    negative_prompt: Optional[str] = Field(
        "blurry, low quality, ugly, bad anatomy, deformed hands,deformed fingers,extra limbs, poorly drawn face",
        description="Negative prompt to avoid unwanted features"
    )
    num_inference_steps: int = Field(50, ge=1, le=100, description="Number of denoising steps")
    guidance_scale: float = Field(7.5, ge=1.0, le=20.0, description="Guidance scale for prompt adherence")
    height: int = Field(768, ge=256, le=2048, description="Image height in pixels")
    width: int = Field(768, ge=256, le=2048, description="Image width in pixels")
    output_dir: str = Field("scheduler_outputs", description="Directory to save the output image")
    filename_prefix: str = Field("single_scheduler", description="Prefix for output filename")

class SingleSchedulerResponse(BaseModel):
    message: str
    output_path: str
    filename: str
    scheduler_used: str

@app.on_event("startup")
async def startup_event():
    """Initialize the pipeline when the API starts."""
    try:
        initialize_pipeline()
        print("Pipeline initialized successfully")
    except Exception as e:
        print(f"Failed to initialize pipeline: {e}")
        raise e

@app.post("/generate", response_model=ImageGenerationResponse)
async def generate_image_endpoint(request: ImageGenerationRequest):
    """
    Generate an image using Stable Diffusion.
    """
    try:
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.png"
        
        # Generate the image
        output_path = generate_image(
            prompt=request.prompt,
            output_file=filename,
            negative_prompt=request.negative_prompt,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
            height=request.height,
            width=request.width,
            output_dir=request.output_dir,
            upscale=request.upscale,
            upscale_prompt=request.upscale_prompt
        )
        
        return ImageGenerationResponse(
            message="Image generated successfully",
            output_path=output_path,
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")

@app.post("/upscale", response_model=UpscaleResponse)
async def upscale_image_endpoint(request: UpscaleRequest):
    """
    Upscale a single image using Stable Diffusion upscaling.
    """
    try:
        from image_upscaling import upscale_image
        
        # Construct full input path
        input_path = os.path.join(request.output_dir, request.input_file)
        
        # Check if input file exists
        if not os.path.exists(input_path):
            raise HTTPException(status_code=404, detail=f"Input file not found: {request.input_file}")
        
        # Generate output filename if not provided
        output_filename = request.output_file
        if output_filename is None:
            base_name = os.path.splitext(request.input_file)[0]
            output_filename = f"{base_name}_upscaled.png"
        
        # Upscale the image
        output_path = upscale_image(
            input_file=input_path,
            prompt=request.prompt,
            output_file=output_filename,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
            output_dir=request.output_dir
        )
        
        return UpscaleResponse(
            message="Image upscaled successfully",
            output_path=output_path,
            filename=output_filename
        )
        
    except ImportError:
        raise HTTPException(status_code=500, detail="Upscaling module not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error upscaling image: {str(e)}")

@app.post("/upscale-directory", response_model=UpscaleDirectoryResponse)
async def upscale_directory_endpoint(request: UpscaleDirectoryRequest):
    """
    Upscale all images in a directory using Stable Diffusion upscaling.
    """
    try:
        from image_upscaling import upscale_directory
        
        # Check if input directory exists
        if not os.path.exists(request.input_directory):
            raise HTTPException(status_code=404, detail=f"Input directory not found: {request.input_directory}")
        
        # Upscale all images in the directory
        output_paths = upscale_directory(
            input_directory=request.input_directory,
            prompt=request.prompt,
            output_directory=request.output_directory,
            file_extensions=request.file_extensions,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale
        )
        
        return UpscaleDirectoryResponse(
            message="Directory upscaling completed successfully",
            output_paths=output_paths,
            total_processed=len(output_paths),
            successful_upscales=len(output_paths)
        )
        
    except ImportError:
        raise HTTPException(status_code=500, detail="Upscaling module not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error upscaling directory: {str(e)}")

@app.post("/upscale-highres", response_model=UpscaleResponse)
async def upscale_high_resolution_endpoint(request: UpscaleHighResolutionRequest):
    """
    High-resolution upscaling using Stable Diffusion (4x) and optionally SwinIR (2x).
    """
    try:
        from image_upscaling import upscale_high_resolution
        
        # Construct full input path
        input_path = os.path.join(request.output_dir, request.input_file)
        
        # Check if input file exists
        if not os.path.exists(input_path):
            raise HTTPException(status_code=404, detail=f"Input file not found: {request.input_file}")
        
        # Generate output filename if not provided
        output_filename = request.output_file
        if output_filename is None:
            base_name = os.path.splitext(request.input_file)[0]
            suffix = "_upscaled_highres_8x.png" if request.use_swinir else "_upscaled_highres_4x.png"
            output_filename = f"{base_name}{suffix}"
        
        # Upscale the image with high resolution
        output_path = upscale_high_resolution(
            input_file=input_path,
            prompt=request.prompt,
            output_file=output_filename,
            output_dir=request.output_dir,
            sd_steps=request.sd_steps,
            sd_guidance_scale=request.sd_guidance_scale,
            use_swinir=request.use_swinir
        )
        
        return UpscaleResponse(
            message="High-resolution upscaling completed successfully",
            output_path=output_path,
            filename=output_filename
        )
        
    except ImportError:
        raise HTTPException(status_code=500, detail="Upscaling module not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in high-resolution upscaling: {str(e)}")


@app.post("/test-schedulers", response_model=SchedulerTestResponse)
async def test_schedulers_endpoint(request: SchedulerTestRequest):
    """
    Test multiple schedulers with the same prompt to compare results.
    """
    try:
        from imagegeneration_schedulers import generate_images_with_schedulers, SCHEDULERS
        
        # Generate images with different schedulers
        results = generate_images_with_schedulers(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
            height=request.height,
            width=request.width,
            output_dir=request.output_dir,
            schedulers_to_test=request.schedulers_to_test,
            filename_prefix=request.filename_prefix
        )
        
        return SchedulerTestResponse(
            message="Scheduler testing completed successfully",
            results=results,
            total_generated=len(results),
            available_schedulers=list(SCHEDULERS.keys())
        )
        
    except ImportError:
        raise HTTPException(status_code=500, detail="Scheduler testing module not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing schedulers: {str(e)}")

@app.post("/generate-single-scheduler", response_model=SingleSchedulerResponse)
async def generate_single_scheduler_endpoint(request: SingleSchedulerRequest):
    """
    Generate an image using a specific scheduler in Stable Diffusion.
    """
    try:
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.png"
        
        # Generate the image with the specified scheduler
        output_path = generate_image(
            prompt=request.prompt,
            output_file=filename,
            negative_prompt=request.negative_prompt,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
            height=request.height,
            width=request.width,
            output_dir=request.output_dir,
            scheduler=request.scheduler_name
        )
        
        return SingleSchedulerResponse(
            message="Image generated successfully with single scheduler",
            output_path=output_path,
            filename=filename,
            scheduler_used=request.scheduler_name
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image with single scheduler: {str(e)}")

@app.post("/generate-scheduler", response_model=SingleSchedulerResponse)
async def generate_with_scheduler_endpoint(request: SingleSchedulerRequest):
    """
    Generate an image using a specific scheduler.
    """
    try:
        from imagegeneration_schedulers import generate_image_with_scheduler, SCHEDULERS
        
        # Validate scheduler name
        if request.scheduler_name not in SCHEDULERS:
            raise HTTPException(
                status_code=400, 
                detail=f"Unknown scheduler '{request.scheduler_name}'. Available schedulers: {list(SCHEDULERS.keys())}"
            )
        
        # Generate the image with the specific scheduler
        output_path = generate_image_with_scheduler(
            prompt=request.prompt,
            scheduler_name=request.scheduler_name,
            negative_prompt=request.negative_prompt,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
            height=request.height,
            width=request.width,
            output_dir=request.output_dir,
            filename_prefix=request.filename_prefix
        )
        
        filename = os.path.basename(output_path)
        
        return SingleSchedulerResponse(
            message=f"Image generated successfully with {request.scheduler_name} scheduler",
            output_path=output_path,
            filename=filename,
            scheduler_used=request.scheduler_name
        )
        
    except ImportError:
        raise HTTPException(status_code=500, detail="Scheduler module not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image with scheduler: {str(e)}")

@app.get("/schedulers")
async def list_schedulers():
    """
    List all available schedulers.
    """
    try:
        from imagegeneration_schedulers import SCHEDULERS
        return {
            "schedulers": list(SCHEDULERS.keys()),
            "total": len(SCHEDULERS),
            "description": "Available schedulers for image generation"
        }
    except ImportError:
        raise HTTPException(status_code=500, detail="Scheduler module not available")

@app.get("/download/{filename}")
async def download_image(filename: str, output_dir: str = "final_outputs"):
    """
    Download a generated image by filename from any output directory.
    """
    # List of possible output directories
    possible_dirs = [output_dir, "final_outputs", "upscaled_outputs", "scheduler_outputs"]
    
    file_path = None
    for directory in possible_dirs:
        potential_path = os.path.join(directory, filename)
        if os.path.exists(potential_path):
            file_path = potential_path
            break
    
    if file_path is None:
        raise HTTPException(
            status_code=404, 
            detail=f"File '{filename}' not found in any output directory: {possible_dirs}"
        )
    
    return FileResponse(
        path=file_path,
        media_type="image/png",
        filename=filename
    )

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "message": "Stable Diffusion API is running"}

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Stable Diffusion Image Generation API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/generate - POST endpoint to generate images",
            "generate-scheduler": "/generate-scheduler - POST endpoint to generate with specific scheduler",
            "upscale": "/upscale - POST endpoint to upscale a single image",
            "upscale-directory": "/upscale-directory - POST endpoint to upscale all images in a directory",
            "upscale-highres": "/upscale-highres - POST endpoint for high-resolution upscaling (4x or 8x)",
            "test-schedulers": "/test-schedulers - POST endpoint to test multiple schedulers",
            "schedulers": "/schedulers - GET endpoint to list available schedulers",
            "files": "/files - GET endpoint to list all generated files",
            "download": "/download/{filename} - GET endpoint to download generated images",
            "health": "/health - GET endpoint for health check",
            "docs": "/docs - Interactive API documentation"
        }
    }

@app.get("/files")
async def list_generated_files():
    """
    List all generated image files across all output directories.
    """
    output_dirs = ["final_outputs", "upscaled_outputs", "scheduler_outputs"]
    files_info = {}
    
    for directory in output_dirs:
        if os.path.exists(directory):
            files = []
            for file in os.listdir(directory):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(directory, file)
                    file_info = {
                        "filename": file,
                        "size_mb": round(os.path.getsize(file_path) / (1024 * 1024), 2),
                        "created": os.path.getctime(file_path),
                        "download_url": f"/download/{file}?output_dir={directory}"
                    }
                    files.append(file_info)
            files_info[directory] = sorted(files, key=lambda x: x["created"], reverse=True)
        else:
            files_info[directory] = []
    
    total_files = sum(len(files) for files in files_info.values())
    
    return {
        "message": f"Found {total_files} generated image files",
        "files": files_info,
        "total_files": total_files
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
