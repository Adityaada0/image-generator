"""
Here we optimized image Generation tool for CPU / integrated GPU systems.
uses Diffusers with CPU optimization and memory efficiency.
"""
import os
import sys
import torch
from diffusers import StableDiffusionPipeline
from pathlib import Path

class ImageGenerator:
    def __init__(self):
        self.pipe = None
        self.provider = None
    
    def build_pipeline(self):
        """Build and configure the image generation pipeline."""
        print("Loading model (this may take a minute on first run)...")
        
        # Use CPU with float32 for compatibility
        device = "cpu"
        dtype = torch.float32
        
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=dtype,
            safety_checker=None,  # Skip safety checker to save memory
            requires_safety_checker=False
        )
        
        self.pipe = self.pipe.to(device)
        
# Memory optimizations for CPU
        self.pipe.enable_attention_slicing()
        print("✓ Pipeline ready (using CPU)")
    
    def generate(self, prompt: str, steps: int = 20, height: int = 512, width: int = 512, output_path: str = "output.png"):
        """Generate an image from a text prompt."""
        if self.pipe is None:
            raise RuntimeError("Pipeline not initialized. Call build_pipeline() first.")
        
        print(f"\n📝 Prompt: {prompt}")
        print(f"⚙️  Settings: {steps} steps, {height}x{width}")
        
        # Warmup (helps with first-run performance)
        print("🔥 Warming up...")
        try:
            self.pipe("warmup", num_inference_steps=1, height=height, width=width)
        except Exception:
            pass
        
        print("🎨 Generating (this will take a few minutes on CPU)...")
        image = self.pipe(
            prompt,
            num_inference_steps=steps,
            height=height,
            width=width,
            guidance_scale=7.5
        ).images[0]
        
        image.save(output_path)
        print(f"✓ Done! Saved to {output_path}")
        return image

if __name__ == "__main__":
    try:
        gen = ImageGenerator()
        gen.build_pipeline()
        
        # ex: usage
        image = gen.generate(
            prompt="a serene mountain landscape with snow, pine trees, and a clear blue sky",
            steps=20,
            height=512,
            width=512
        )
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        print("\nTroubleshooting:", file=sys.stderr)
        print("1. Install required packages:", file=sys.stderr)
        print("   pip install onnxruntime-directml diffusers transformers safetensors accelerate pillow", file=sys.stderr)
        print("2. Ensure your system has 8GB+ RAM available", file=sys.stderr)
        print("3. For Intel CPUs, try: pip install onnxruntime-openvino", file=sys.stderr)
        raise