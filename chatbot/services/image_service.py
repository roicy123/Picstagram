# chatbot/services/image_service.py
import os
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import base64
from io import BytesIO

class ImageGenerationService:
    def __init__(self):
        # Load Stable Diffusion model
        model_id = "stabilityai/stable-diffusion-2-1-base"  # Free HuggingFace model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load model with improvements
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
        )
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        self.pipe = self.pipe.to(self.device)
        
        # Enable memory optimization if on GPU
        if self.device == "cuda":
            self.pipe.enable_attention_slicing()
    
    def generate_image(self, prompt, negative_prompt=""):
        try:
            # Generate image
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=25,
                guidance_scale=7.5,
                width=512,
                height=512,
            ).images[0]
            
            # Convert to base64 for web display
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            return {
                "status": "success",
                "image": img_str
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }