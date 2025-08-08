# 🎨 Streamlit Web Interface Guide

## 🌟 Welcome to Stable Diffusion Studio!

The Streamlit web interface provides a beautiful, user-friendly way to interact with the Stable Diffusion API. No coding required - just point, click, and create!

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
# Start both services
./deploy.sh deploy

# Access the interface
open http://localhost:8501
```

### Option 2: Local Development
```bash
# Start locally without Docker
./run_local.sh

# Access the interface
open http://localhost:8501
```

## 🎯 Main Features

### 1. 🎨 **Generate Images**
- **Simple Interface**: Enter prompts using natural language
- **Real-time Parameters**: Adjust settings with sliders and dropdowns
- **Instant Preview**: See your generated images immediately
- **Auto-download**: Save images with one click

**Example workflow:**
1. Navigate to "Generate Images"
2. Enter: "A beautiful sunset over mountains, digital art"
3. Adjust image size and quality settings
4. Click "Generate Image"
5. Download your creation!

### 2. 🔧 **Advanced Generation**
- **Scheduler Selection**: Choose from 17+ different AI schedulers
- **Fine-tuned Control**: Precise control over generation parameters
- **Seed Control**: Reproducible results with custom seeds
- **Higher Resolution**: Generate larger, more detailed images

**Pro tip:** Try different schedulers like `EulerDiscrete` for speed or `DDIM` for quality!

### 3. 📊 **Compare Schedulers**
- **Side-by-side Comparison**: Generate the same prompt with multiple schedulers
- **Visual Analysis**: See differences in style, quality, and detail
- **Scheduler Learning**: Understand which works best for your use case

**Perfect for:** Finding your preferred scheduler for different art styles

### 4. ⬆️ **Upscale Images**
- **4x Enhancement**: Improve resolution and detail of any generated image
- **AI-powered**: Intelligent upscaling that adds realistic details
- **Before/After View**: Compare original vs enhanced versions
- **Custom Enhancement**: Add specific enhancement prompts

**Use cases:** Making wallpapers, prints, or professional-quality images

### 5. 📁 **File Management & Gallery**
- **Visual Gallery**: Browse all your generated images
- **Organized Display**: Paginated view of your creations
- **Easy Downloads**: One-click download for any image
- **Image Details**: View resolution, format, and metadata

## 🎨 Interface Walkthrough

### Navigation Sidebar
The left sidebar contains:
- **Task Selection**: Choose what you want to do
- **Tips & Guides**: Helpful information for each feature
- **Quick Links**: Direct access to tools and documentation

### Main Content Area
- **Input Forms**: User-friendly forms for all parameters
- **Real-time Feedback**: Progress indicators and status updates
- **Results Display**: Generated images with download options
- **Interactive Elements**: Sliders, dropdowns, and buttons

### Status & Feedback
- **Connection Status**: Shows if the API backend is running
- **Progress Indicators**: Visual feedback during generation
- **Error Messages**: Clear explanations if something goes wrong
- **Success Notifications**: Confirmation when operations complete

## 🛠️ Parameter Guide

### Basic Parameters
- **Prompt**: Describe what you want to see
- **Negative Prompt**: Describe what you want to avoid
- **Width/Height**: Image dimensions (512, 768, 1024)
- **Inference Steps**: Quality vs speed (10-50, default: 20)
- **Guidance Scale**: How closely to follow the prompt (1-20, default: 7.5)

### Advanced Parameters
- **Scheduler**: Algorithm used for generation
- **Seed**: For reproducible results (0 = random)
- **Enhancement Prompt**: For upscaling improvements

## 💡 Tips for Best Results

### Prompt Writing
```
Good: "A serene mountain lake at sunset, realistic photography, high detail"
Better: "A crystal-clear mountain lake reflecting orange sunset clouds, shot with DSLR, photorealistic, 8K resolution"
```

### Parameter Optimization
- **Quick Tests**: Use 10-15 steps for fast iteration
- **Final Images**: Use 25-50 steps for best quality
- **Small to Large**: Generate 512x512 first, then upscale
- **Negative Prompts**: Always include "blurry, low quality, distorted"

### Scheduler Selection
- **EulerDiscrete**: Fast, good for most images
- **DDIM**: High quality, slightly slower
- **DPMSolverMultistep**: Good balance of speed and quality
- **LMSDiscrete**: Great for artistic styles

## 🔧 Troubleshooting

### Common Issues

**"FastAPI service is not running"**
- Start the backend: `./deploy.sh start`
- Check Docker: `docker ps`
- View logs: `./deploy.sh logs`

**Generation taking too long**
- Reduce inference steps (try 10-15)
- Use smaller image size (512x512)
- Check GPU memory with `nvidia-smi`

**Images not appearing**
- Check browser console for errors
- Refresh the page
- Verify file permissions in output directories

**Interface not loading**
- Ensure port 8501 is not blocked
- Try accessing via `http://127.0.0.1:8501`
- Check Streamlit logs in terminal

### Performance Tips
- **GPU Memory**: Monitor with `nvidia-smi`
- **Concurrent Users**: One generation at a time for best performance
- **File Storage**: Regularly clean up old images to save space
- **Browser**: Use Chrome or Firefox for best compatibility

## 🌐 Accessing Remote Instances

If running on a remote server:

```bash
# Replace YOUR_SERVER_IP with actual IP
http://YOUR_SERVER_IP:8501
```

**Security note**: Only expose these ports on trusted networks!

## 🎉 Getting Help

- **Built-in Tips**: Each tab has helpful tips in the sidebar
- **API Documentation**: Available at `http://localhost:8000/docs`
- **Error Messages**: The interface provides clear error descriptions
- **Logs**: Check terminal output for detailed debugging

## 🚀 Next Steps

Once you're comfortable with the interface:

1. **Experiment**: Try different combinations of prompts and settings
2. **Save Favorites**: Download your best creations
3. **Share**: Show off your AI art!
4. **API Integration**: Use the FastAPI directly for automation
5. **Customize**: Modify the Streamlit code for your specific needs

---

**🎨 Happy Creating!**

Your Streamlit interface is ready at: **http://localhost:8501**
