# 🎨 Swagger UI Testing Guide for Stable Diffusion API

## 🌐 Accessing Swagger UI

Your FastAPI service automatically provides interactive API documentation through Swagger UI. This is the **recommended way** to test your API instead of using curl commands.

### Quick Start

1. **Deploy your service:**
   ```bash
   ./quick_test.sh
   # or
   ./deploy.sh deploy
   ```

2. **Open Swagger UI:**
   - **Primary**: http://localhost:8000/docs (Swagger UI)
   - **Alternative**: http://localhost:8000/redoc (ReDoc)
   - **API Spec**: http://localhost:8000/openapi.json

3. **Interactive Testing Helper:**
   ```bash
   python3 swagger_tester.py
   ```

## 🎯 How to Use Swagger UI

### 1. **Explore the Interface**
- **Endpoint List**: All available endpoints are listed by category
- **Expand Sections**: Click on any endpoint to see details
- **Schemas**: View request/response models at the bottom

### 2. **Test an Endpoint**
1. Click on any endpoint (e.g., `POST /generate`)
2. Click **"Try it out"** button
3. Modify the request parameters/body
4. Click **"Execute"** 
5. View the response in real-time

### 3. **Common Testing Scenarios**

#### A) 🖼️ Generate a Simple Image
**Endpoint**: `POST /generate`

**Sample Request Body:**
```json
{
  "prompt": "a beautiful sunset over mountains, digital art",
  "negative_prompt": "blurry, low quality, ugly",
  "num_inference_steps": 20,
  "guidance_scale": 7.5,
  "height": 512,
  "width": 512,
  "upscale": false
}
```

#### B) 🎛️ Generate with Specific Scheduler
**Endpoint**: `POST /generate-scheduler`

**Sample Request Body:**
```json
{
  "prompt": "cyberpunk city at night, neon lights",
  "scheduler_name": "EulerDiscrete",
  "num_inference_steps": 25,
  "guidance_scale": 8.0,
  "height": 768,
  "width": 768
}
```

#### C) 🔍 Compare Multiple Schedulers
**Endpoint**: `POST /test-schedulers`

**Sample Request Body:**
```json
{
  "prompt": "a serene forest path in autumn",
  "schedulers_to_test": ["EulerDiscrete", "DDIM", "DPMSolverMultistep"],
  "num_inference_steps": 20,
  "filename_prefix": "forest_comparison"
}
```

#### D) ⬆️ Upscale an Image
**Endpoint**: `POST /upscale`

**Sample Request Body:**
```json
{
  "input_file": "your_generated_image.png",
  "prompt": "enhance details, high quality, sharp",
  "num_inference_steps": 50,
  "guidance_scale": 7.5
}
```

## 📋 Step-by-Step Testing Workflow

### 1. **Start with Basic Endpoints**
1. Test `GET /health` - Verify service is running
2. Test `GET /schedulers` - See available schedulers  
3. Test `GET /files` - Check existing files

### 2. **Generate Your First Image**
1. Go to `POST /generate`
2. Use simple parameters:
   ```json
   {
     "prompt": "a simple test image",
     "num_inference_steps": 10,
     "height": 512,
     "width": 512
   }
   ```
3. Click "Execute" and wait for response
4. Note the `filename` in the response

### 3. **Download the Generated Image**
1. Go to `GET /download/{filename}`
2. Enter the filename from step 2
3. Click "Execute" 
4. Click "Download file" in the response

### 4. **Test Advanced Features**
1. Try different schedulers with `POST /generate-scheduler`
2. Compare schedulers with `POST /test-schedulers`
3. Upscale images with `POST /upscale`

## 🔧 Swagger UI Features

### **Request Customization**
- ✅ Modify any parameter in the request body
- ✅ See parameter descriptions and constraints
- ✅ Use example values or create your own
- ✅ Validate input before sending

### **Response Analysis**
- ✅ View HTTP status codes and meanings
- ✅ See response headers and body
- ✅ Download files directly from responses
- ✅ Copy curl commands for future use

### **Schema Exploration**
- ✅ View all request/response models
- ✅ Understand required vs optional fields
- ✅ See data types and validation rules
- ✅ Explore nested object structures

## 🎨 Quick Testing Shortcuts

### **Fast Image Generation**
For quick testing, use these optimized parameters:
```json
{
  "prompt": "your prompt here",
  "num_inference_steps": 10,
  "height": 512,
  "width": 512
}
```

### **Scheduler Testing**
Test popular schedulers:
- `EulerDiscrete` - Fast and stable
- `DDIM` - High quality
- `DPMSolverMultistep` - Good balance

### **File Management**
1. `GET /files` - List all generated images
2. `GET /download/{filename}` - Download specific image
3. Use filenames from the `/files` response

## 🚀 Deployment Commands

### **Start Service with Swagger UI**
```bash
# One-command deploy and open Swagger UI
./quick_test.sh

# Or step by step:
./deploy.sh deploy
# Then open http://localhost:8000/docs
```

### **Interactive Testing Helper**
```bash
# Launch interactive testing menu
python3 swagger_tester.py
```

### **Service Management**
```bash
./deploy.sh start    # Start service
./deploy.sh stop     # Stop service
./deploy.sh logs     # View logs
./deploy.sh restart  # Restart service
```

## 🔍 Troubleshooting

### **Common Issues**

**Service not responding:**
1. Check health: `GET /health`
2. View logs: `./deploy.sh logs`
3. Restart: `./deploy.sh restart`

**Generation taking too long:**
- Reduce `num_inference_steps` (try 10-20)
- Use smaller image sizes (512x512)
- Check GPU memory with `nvidia-smi`

**File not found errors:**
- Use `GET /files` to see available files
- Check the exact filename spelling
- Ensure the file exists in the correct directory

### **Validation Errors (422)**
- Check parameter types (numbers vs strings)
- Verify required fields are provided
- Check min/max value constraints
- Use the schema reference at the bottom

## 💡 Pro Tips

1. **Use the Schema Reference**: Scroll down in Swagger UI to see all data models
2. **Copy Curl Commands**: Each executed request shows the equivalent curl command
3. **Bookmark URLs**: Save direct links to frequently used endpoints
4. **Test Incrementally**: Start simple, then add complexity
5. **Monitor Resources**: Keep an eye on GPU memory usage
6. **Save Responses**: Copy important response data for your records

## 🎯 Next Steps

Once you're comfortable with Swagger UI:
1. **Integrate with your application** using the API
2. **Automate workflows** with the provided Python scripts
3. **Scale up** with more complex prompts and parameters
4. **Deploy to production** following the deployment guide

---

**🎉 Happy Testing with Swagger UI!**

Your interactive API documentation is now ready at: http://localhost:8000/docs
