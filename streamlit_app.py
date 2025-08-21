#!/usr/bin/env python3
"""
Streamlit Frontend for Stable Diffusion FastAPI Service

This provides a user-friendly web interface for all FastAPI endpoints including:
- Image generation with various schedulers
- Image upscaling
- Scheduler comparison
- File management and downloads
"""

import streamlit as st
import requests
import json
import io
from PIL import Image
import time
import os
from typing import List, Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"
STREAMLIT_PORT = 8501

class StableDiffusionUI:
    def __init__(self):
        self.api_base = API_BASE_URL
        
    def check_api_health(self):
        """Check if the FastAPI service is running."""
        try:
            response = requests.get(f"{self.api_base}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_schedulers(self):
        """Get list of available schedulers."""
        try:
            response = requests.get(f"{self.api_base}/schedulers")
            if response.status_code == 200:
                return response.json().get("schedulers", [])
        except:
            pass
        return []
    
    def get_available_files(self):
        """Get list of generated files."""
        try:
            response = requests.get(f"{self.api_base}/files")
            if response.status_code == 200:
                data = response.json()
                files = data.get("files", [])
                # Ensure we return a list of strings
                if isinstance(files, list):
                    return [str(f) for f in files if f]
                else:
                    return []
        except Exception as e:
            st.error(f"Error fetching files: {e}")
        return []
    
    def generate_image(self, params: Dict[str, Any]):
        """Generate image using basic endpoint."""
        try:
            response = requests.post(f"{self.api_base}/generate", json=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Error generating image: {e}")
            return None
    
    def generate_with_scheduler(self, params: Dict[str, Any]):
        """Generate image with specific scheduler."""
        try:
            response = requests.post(f"{self.api_base}/generate-scheduler", json=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Error generating image with scheduler: {e}")
            return None
    
    def test_schedulers(self, params: Dict[str, Any]):
        """Test multiple schedulers."""
        try:
            response = requests.post(f"{self.api_base}/test-schedulers", json=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Error testing schedulers: {e}")
            return None
    
    def upscale_image(self, params: Dict[str, Any]):
        """Upscale a single image."""
        try:
            response = requests.post(f"{self.api_base}/upscale", json=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Error upscaling image: {e}")
            return None
    
    def download_image(self, filename: str):
        """Download an image file."""
        try:
            response = requests.get(f"{self.api_base}/download/{filename}")
            if response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
        except Exception as e:
            st.error(f"Error downloading image: {e}")
        return None

def main():
    st.set_page_config(
        page_title="Stable Diffusion Studio",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize the UI class
    ui = StableDiffusionUI()
    
    # Header
    st.title("🎨 Stable Diffusion Studio")
    st.markdown("**Interactive AI Image Generation & Processing**")
    
    # Check API health
    if not ui.check_api_health():
        st.error("🚨 FastAPI service is not running! Please start the service first.")
        st.code("./deploy.sh start")
        st.stop()
    
    st.success("✅ Connected to FastAPI service")
    
    # Sidebar navigation
    st.sidebar.title("🎛️ Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose your task:",
        [
            "🎨 Generate Images",
            "🔧 Advanced Generation",
            "📊 Compare Schedulers", 
            "⬆️ Upscale Images",
            "📁 File Management",
            "ℹ️ About"
        ]
    )
    
    # Main content based on selection
    if app_mode == "🎨 Generate Images":
        generate_images_tab(ui)
    elif app_mode == "🔧 Advanced Generation":
        advanced_generation_tab(ui)
    elif app_mode == "📊 Compare Schedulers":
        compare_schedulers_tab(ui)
    elif app_mode == "⬆️ Upscale Images":
        upscale_images_tab(ui)
    elif app_mode == "📁 File Management":
        file_management_tab(ui)
    elif app_mode == "ℹ️ About":
        about_tab()

def generate_images_tab(ui):
    """Basic image generation interface."""
    st.header("🎨 Generate Images")
    st.markdown("Create beautiful AI-generated images with simple prompts.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input parameters
        prompt = st.text_area(
            "✨ Describe your image:",
            placeholder="A beautiful sunset over mountains, digital art style...",
            height=100
        )
        
        negative_prompt = st.text_area(
            "🚫 What to avoid:",
            placeholder="blurry, low quality, ugly, distorted...",
            height=60
        )
        
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            width = st.selectbox("Width", [512, 768, 1024], index=0)
            num_steps = st.slider("Inference Steps", 10, 50, 20)
        with col1_2:
            height = st.selectbox("Height", [512, 768, 1024], index=0)
            guidance_scale = st.slider("Guidance Scale", 1.0, 20.0, 7.5, 0.5)
        
        upscale_option = st.checkbox("🔍 Auto-upscale result (4x)")
        
        if st.button("🚀 Generate Image", type="primary", use_container_width=True):
            if not prompt.strip():
                st.error("Please enter a prompt!")
                return
                
            params = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "width": width,
                "height": height,
                "num_inference_steps": num_steps,
                "guidance_scale": guidance_scale,
                "upscale": upscale_option
            }
            
            with st.spinner("🎨 Creating your masterpiece..."):
                result = ui.generate_image(params)
            
            if result:
                st.success(f"✅ Image generated: {result['filename']}")
                display_generated_image(ui, result['filename'])
            else:
                st.error("Failed to generate image")
    
    with col2:
        st.markdown("### 💡 Tips")
        st.info("""
        **Prompt Tips:**
        - Be specific and descriptive
        - Include style keywords (e.g., "digital art", "photorealistic")
        - Mention lighting, colors, mood
        
        **Parameters:**
        - **Steps**: More = better quality, slower
        - **Guidance**: Higher = follows prompt more closely
        - **Size**: Larger = more detail, more memory
        """)

def advanced_generation_tab(ui):
    """Advanced generation with scheduler selection."""
    st.header("🔧 Advanced Image Generation")
    st.markdown("Fine-tune your image generation with specific schedulers and advanced options.")
    
    # Get available schedulers
    schedulers = ui.get_available_schedulers()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        prompt = st.text_area(
            "✨ Image prompt:",
            placeholder="cyberpunk city at night, neon lights, highly detailed...",
            height=100
        )
        
        negative_prompt = st.text_area(
            "🚫 Negative prompt:",
            placeholder="blurry, low quality, ugly...",
            height=60
        )
        
        # Scheduler selection
        if schedulers:
            scheduler_name = st.selectbox("🎛️ Scheduler:", schedulers)
        else:
            scheduler_name = st.text_input("🎛️ Scheduler:", value="EulerDiscrete")
        
        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            width = st.selectbox("Width", [512, 768, 1024], index=1)
            height = st.selectbox("Height", [512, 768, 1024], index=1)
        with col1_2:
            num_steps = st.slider("Inference Steps", 10, 100, 25)
            guidance_scale = st.slider("Guidance Scale", 1.0, 20.0, 8.0, 0.5)
        with col1_3:
            seed = st.number_input("Seed (optional)", value=0, help="0 = random seed")
        
        if st.button("🎯 Generate with Scheduler", type="primary", use_container_width=True):
            if not prompt.strip():
                st.error("Please enter a prompt!")
                return
                
            params = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "scheduler_name": scheduler_name,
                "width": width,
                "height": height,
                "num_inference_steps": num_steps,
                "guidance_scale": guidance_scale
            }
            
            if seed > 0:
                params["seed"] = seed
            
            with st.spinner(f"🎨 Generating with {scheduler_name}..."):
                result = ui.generate_with_scheduler(params)
            
            if result:
                st.success(f"✅ Image generated: {result['filename']}")
                display_generated_image(ui, result['filename'])
            else:
                st.error("Failed to generate image")
    
    with col2:
        st.markdown("### 🎛️ Scheduler Guide")
        scheduler_info = {
            "EulerDiscrete": "Fast and stable, good for most images",
            "DDIM": "High quality, deterministic results",
            "DPMSolverMultistep": "Good balance of speed and quality",
            "LMSDiscrete": "Smooth results, good for artistic styles",
            "PNDM": "Original DDPM scheduler, stable",
            "DDPMScheduler": "Classic diffusion, longer generation",
            "UniPCMultistep": "Fast convergence, good quality"
        }
        
        for scheduler, description in scheduler_info.items():
            st.info(f"**{scheduler}**: {description}")

def compare_schedulers_tab(ui):
    """Compare multiple schedulers side by side."""
    st.header("📊 Compare Schedulers")
    st.markdown("Generate the same image with different schedulers to compare results.")
    
    schedulers = ui.get_available_schedulers()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        prompt = st.text_area(
            "✨ Prompt for comparison:",
            placeholder="a serene forest path in autumn, detailed, beautiful lighting...",
            height=100
        )
        
        if schedulers:
            selected_schedulers = st.multiselect(
                "🎛️ Select schedulers to compare:",
                schedulers,
                default=schedulers[:3] if len(schedulers) >= 3 else schedulers
            )
        else:
            st.warning("No schedulers available from API")
            selected_schedulers = []
        
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            num_steps = st.slider("Inference Steps", 10, 50, 20)
            guidance_scale = st.slider("Guidance Scale", 1.0, 20.0, 7.5, 0.5)
        with col1_2:
            filename_prefix = st.text_input("Filename prefix:", value="comparison")
        
        if st.button("🔍 Compare Schedulers", type="primary", use_container_width=True):
            if not prompt.strip():
                st.error("Please enter a prompt!")
                return
            if not selected_schedulers:
                st.error("Please select at least one scheduler!")
                return
                
            params = {
                "prompt": prompt,
                "schedulers_to_test": selected_schedulers,
                "num_inference_steps": num_steps,
                "guidance_scale": guidance_scale,
                "filename_prefix": filename_prefix
            }
            
            with st.spinner(f"🔍 Comparing {len(selected_schedulers)} schedulers..."):
                result = ui.test_schedulers(params)
            
            if result:
                st.success(f"✅ Scheduler comparison completed!")
                
                # The actual API returns a dict with scheduler names as keys and file paths as values
                # Extract filenames from the full paths
                if isinstance(result, dict):
                    st.subheader("📊 Comparison Results")
                    
                    # Handle different possible response formats
                    files_dict = {}
                    if "results" in result:
                        files_dict = result["results"]
                    elif "generated_files" in result:
                        # If it's the expected format
                        files_dict = {item["scheduler"]: item["filename"] for item in result["generated_files"]}
                    else:
                        # If the result itself is the files dict
                        files_dict = result
                    
                    if files_dict:
                        # Display images in columns
                        num_cols = min(3, len(files_dict))
                        cols = st.columns(num_cols)
                        
                        for i, (scheduler_name, file_path) in enumerate(files_dict.items()):
                            with cols[i % num_cols]:
                                st.markdown(f"**{scheduler_name}**")
                                
                                # Extract filename from path if needed
                                filename = file_path
                                if "/" in file_path:
                                    filename = file_path.split("/")[-1]
                                
                                # Try to download and display the image
                                img = ui.download_image(filename)
                                if img:
                                    st.image(img, use_column_width=True)
                                    st.download_button(
                                        f"⬇️ Download",
                                        data=download_image_bytes(ui, filename),
                                        file_name=filename,
                                        mime="image/png",
                                        key=f"download_{scheduler_name}_{i}"
                                    )
                                else:
                                    st.error(f"Could not load image: {filename}")
                                    st.text(f"Full path: {file_path}")
                    else:
                        st.error("No images found in response")
                        st.json(result)  # Debug: show the actual response
                else:
                    st.error("Unexpected response format")
                    st.json(result)  # Debug: show the actual response
            else:
                st.error("Failed to generate comparison images")
    
    with col2:
        st.markdown("### 📊 Comparison Tips")
        st.info("""
        **What to look for:**
        - Image sharpness and detail
        - Color accuracy and saturation
        - Adherence to the prompt
        - Artistic style and coherence
        - Generation time differences
        
        **Best practices:**
        - Use the same prompt for fair comparison
        - Keep parameters consistent
        - Try different types of prompts (realistic, artistic, etc.)
        """)

def upscale_images_tab(ui):
    """Image upscaling interface."""
    st.header("⬆️ Upscale Images")
    st.markdown("Enhance your generated images with AI upscaling.")
    
    files = ui.get_available_files()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if files:
            selected_file = st.selectbox("📁 Select image to upscale:", files)
            
            # Display selected image
            if selected_file:
                img = ui.download_image(selected_file)
                if img:
                    st.image(img, caption=f"Original: {selected_file}", width=300)
        else:
            st.warning("No images available. Generate some images first!")
            return
        
        # Upscaling parameters
        enhancement_prompt = st.text_area(
            "🎨 Enhancement prompt:",
            placeholder="enhance details, high quality, sharp, photorealistic...",
            help="Describe how you want to enhance the image"
        )
        
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            num_steps = st.slider("Inference Steps", 20, 100, 50)
        with col1_2:
            guidance_scale = st.slider("Guidance Scale", 1.0, 20.0, 7.5, 0.5)
        
        if st.button("🚀 Upscale Image", type="primary", use_container_width=True):
            params = {
                "input_file": selected_file,
                "prompt": enhancement_prompt,
                "num_inference_steps": num_steps,
                "guidance_scale": guidance_scale
            }
            
            with st.spinner("⬆️ Upscaling image (this may take a while)..."):
                result = ui.upscale_image(params)
            
            if result:
                st.success(f"✅ Image upscaled: {result['upscaled_filename']}")
                
                # Display before/after comparison
                st.subheader("🔍 Before vs After")
                col_before, col_after = st.columns(2)
                
                with col_before:
                    st.markdown("**Before (Original)**")
                    if img:
                        st.image(img, use_column_width=True)
                
                with col_after:
                    st.markdown("**After (Upscaled)**")
                    upscaled_img = ui.download_image(result['upscaled_filename'])
                    if upscaled_img:
                        st.image(upscaled_img, use_column_width=True)
                        st.download_button(
                            "⬇️ Download Upscaled",
                            data=download_image_bytes(ui, result['upscaled_filename']),
                            file_name=result['upscaled_filename'],
                            mime="image/png"
                        )
            else:
                st.error("Failed to upscale image")
    
    with col2:
        st.markdown("### ⬆️ Upscaling Guide")
        st.info("""
        **Enhancement Tips:**
        - Use descriptive enhancement prompts
        - "high quality", "detailed", "sharp" work well
        - Mention specific improvements you want
        - More steps = better quality (but slower)
        
        **Expected Results:**
        - 4x resolution increase
        - Enhanced details and sharpness
        - Improved overall quality
        - Larger file size
        """)

def file_management_tab(ui):
    """File management and gallery."""
    st.header("📁 File Management & Gallery")
    st.markdown("Browse, download, and manage your generated images.")
    
    files = ui.get_available_files()
    
    # Handle case where files might not be a list or might be None
    if not files or not isinstance(files, list):
        st.info("No images generated yet. Create some images first!")
        return
    
    if len(files) == 0:
        st.info("No images available. Generate some images first!")
        return
    
    st.markdown(f"**📊 Total files: {len(files)}**")
    
    # Gallery view
    st.subheader("🖼️ Image Gallery")
    
    # Pagination
    items_per_page = 6
    total_pages = max(1, (len(files) - 1) // items_per_page + 1)
    
    if total_pages > 1:
        page = st.selectbox("📄 Page:", range(1, total_pages + 1)) - 1
    else:
        page = 0
    
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, len(files))
    
    # Ensure we don't go out of bounds
    if start_idx >= len(files):
        st.error("Page out of range")
        return
        
    current_files = files[start_idx:end_idx]
    
    # Display images in grid
    cols = st.columns(3)
    for i, filename in enumerate(current_files):
        with cols[i % 3]:
            try:
                img = ui.download_image(filename)
                if img:
                    st.image(img, caption=filename, use_column_width=True)
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button(f"🔍 View", key=f"view_{filename}"):
                            display_image_details(ui, filename)
                    with col_btn2:
                        st.download_button(
                            "⬇️ Download",
                            data=download_image_bytes(ui, filename),
                            file_name=filename,
                            mime="image/png",
                            key=f"download_{filename}"
                        )
                else:
                    st.error(f"Could not load image: {filename}")
            except Exception as e:
                st.error(f"Error displaying {filename}: {str(e)}")

def about_tab():
    """About and help information."""
    st.header("ℹ️ About Stable Diffusion Studio")
    
    st.markdown("""
    ## 🎨 Welcome to Stable Diffusion Studio!
    
    This is a user-friendly web interface for the Stable Diffusion FastAPI service. 
    It provides easy access to all the powerful AI image generation capabilities.
    
    ### ✨ Features
    - **Simple Image Generation**: Create images with basic prompts
    - **Advanced Controls**: Fine-tune with schedulers and parameters  
    - **Scheduler Comparison**: Test different algorithms side-by-side
    - **Image Upscaling**: Enhance your images with AI upscaling
    - **File Management**: Browse and download all your creations
    
    ### 🚀 Quick Start Guide
    1. **Generate**: Start with the "Generate Images" tab
    2. **Experiment**: Try different prompts and settings
    3. **Compare**: Use "Compare Schedulers" to find your favorite
    4. **Enhance**: Upscale your best images for higher quality
    5. **Download**: Save your favorites from the gallery
    
    ### 🎛️ API Endpoints Used
    - `POST /generate` - Basic image generation
    - `POST /generate-scheduler` - Advanced generation with scheduler
    - `POST /test-schedulers` - Multi-scheduler comparison
    - `POST /upscale` - Image upscaling
    - `GET /files` - File listing
    - `GET /download/{filename}` - Image download
    - `GET /schedulers` - Available schedulers
    - `GET /health` - Service health check
    
    ### 💡 Tips for Best Results
    - **Be specific** in your prompts
    - **Experiment** with different schedulers
    - **Use negative prompts** to avoid unwanted elements
    - **Start small** then upscale for final results
    - **Save your favorites** by downloading them
    
    ### 🔧 Technical Details
    - **Backend**: FastAPI with GPU acceleration
    - **Frontend**: Streamlit web interface
    - **AI Models**: Stable Diffusion variants
    - **Upscaling**: AI-powered enhancement
    - **Docker**: Containerized deployment
    """)
    
    st.markdown("---")
    st.markdown("**🎉 Happy creating!** If you encounter any issues, check the FastAPI service logs.")

def display_generated_image(ui, filename):
    """Display a generated image with download option."""
    img = ui.download_image(filename)
    if img:
        st.image(img, caption=filename, use_column_width=True)
        st.download_button(
            "⬇️ Download Image",
            data=download_image_bytes(ui, filename),
            file_name=filename,
            mime="image/png"
        )

def display_image_details(ui, filename):
    """Display detailed view of an image."""
    st.subheader(f"🔍 {filename}")
    img = ui.download_image(filename)
    if img:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.image(img, use_column_width=True)
        with col2:
            st.markdown(f"**Filename:** {filename}")
            st.markdown(f"**Size:** {img.size[0]} x {img.size[1]}")
            st.markdown(f"**Format:** {img.format}")
            
            st.download_button(
                "⬇️ Download Full Size",
                data=download_image_bytes(ui, filename),
                file_name=filename,
                mime="image/png"
            )

def download_image_bytes(ui, filename):
    """Get image as bytes for download."""
    try:
        response = requests.get(f"{ui.api_base}/download/{filename}")
        if response.status_code == 200:
            return response.content
    except:
        pass
    return b""

if __name__ == "__main__":
    main()
