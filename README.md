# CPU/Integrated GPU Image Generator

A lightweight, optimized image generation tool designed for systems **without a dedicated GPU**. Uses ONNX Runtime with DirectML acceleration on Windows.

## 🎯 What You Get

- **Fast CPU generation**: Optimized for integrated GPUs (Intel Iris, AMD Radeon, etc.)
- **DirectML support**: Leverages Windows GPU acceleration without CUDA
- **Web UI**: Simple, modern interface for generating images
- **Memory efficient**: Runs on systems with 8GB+ RAM
- **Configurable**: Adjust steps, resolution for speed vs. quality

## ⚙️ System Requirements

- **RAM**: 8GB minimum (16GB recommended)
- **CPU**: Dual-core or better
- **Disk**: ~10GB free (for models)
- **Windows 7+** (or Linux with ONNX CPU)
- **Python 3.8+**

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
# Open PowerShell and run:
pip install -r requirements.txt
```

**For Windows with integrated GPU (recommended):**
- Intel Iris: Automatically uses DirectML
- AMD Radeon: Automatically uses DirectML
- NVIDIA (no CUDA): Falls back to CPU, but you could use CUDA if available

### 2. Run the Web Interface

```powershell
python app.py
```

Then open your browser to: **http://localhost:5000**

### 3. Or Use Directly from Python

```python
from generate import ImageGenerator

gen = ImageGenerator()
gen.build_pipeline()

image = gen.generate(
    prompt="a beautiful mountain landscape",
    steps=20,
    height=512,
    width=512
)
```

## 📊 Performance Tips

### For Maximum Speed:
- **Reduce steps**: 10-15 (draft quality)
- **Reduce resolution**: 384x384 or 256x256
- **Use DirectML**: Install `onnxruntime-directml`

### For Best Quality:
- **More steps**: 30-50 (slower)
- **Higher resolution**: 768x768
- **Trade-off**: ~2-5 minutes on CPU, ~30-60 sec on integrated GPU

### Typical Generation Times (Intel i5 + 8GB RAM):
- 512x512, 20 steps: 3-5 minutes
- 512x512, 10 steps: 1.5-2 minutes
- 384x384, 15 steps: 1-1.5 minutes

## 🔧 Advanced Configuration

### Use OpenVINO (Intel CPUs)
```powershell
pip install onnxruntime-openvino
```

### Check Available Acceleration
```python
import onnxruntime as ort
print(ort.get_available_providers())
# Output: ['DmlExecutionProvider', 'CPUExecutionProvider'] (Windows + iGPU)
# Output: ['CPUExecutionProvider'] (Windows, no iGPU)
```

### Run Without Web UI (CLI)
```powershell
python generate.py
```

## 📁 File Structure

```
image-generator/
├── generate.py          # Core image generation class
├── app.py              # Flask web server
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── templates/
│   └── index.html      # Web UI
└── outputs/            # Generated images saved here
```

## ❌ Troubleshooting

### "out of memory" error
- Reduce height/width to 384x384 or 256x256
- Reduce inference steps to 10-15
- Close other applications

### Very slow generation (>10 minutes)
- Not using DirectML → Install `onnxruntime-directml`
- Too many steps → Reduce to 15-20
- Too high resolution → Use 512x512 instead of 768x768

### Model fails to download
- Check internet connection
- ~4GB download required for model
- Try again, it will resume if interrupted

### Flask server won't start
```powershell
pip install flask==2.3.3
```

## 📝 API Endpoint

If building your own UI:

```
POST /api/generate
Content-Type: application/json

{
  "prompt": "a beautiful landscape",
  "steps": 20,
  "height": 512,
  "width": 512
}

Response:
{
  "success": true,
  "image": "data:image/png;base64,..."
}
```

## 🎓 Model Information

- **Base Model**: Stable Diffusion v1.5 (ONNX)
- **Weights**: ~4GB on disk
- **Cached locally** in: `~/.cache/huggingface/diffusers/`

## 📌 Notes

- First run will download the model (4GB) - be patient!
- Generation time varies based on CPU and RAM speed
- Integrated GPU (DirectML) gives 2-3x speedup over pure CPU
- For NVIDIA GPUs, consider using ` torch ` + `cuda ` instead (different setup)

## 🤝 Contributing

Feel free to optimize further for your specific hardware !

Enjoy generating images ! 🎨
