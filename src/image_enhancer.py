"""Image enhancement module using AI models."""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Optional, Union
import logging

try:
    from realesrgan import RealESRGANer
    from basicsr.archs.rrdbnet_arch import RRDBNet
    REALESRGAN_AVAILABLE = True
except ImportError:
    REALESRGAN_AVAILABLE = False
    logging.warning("Real-ESRGAN not available. Using basic upscaling methods.")

import config

class ImageEnhancer:
    """AI-powered image enhancement class."""
    
    def __init__(self):
        """Initialize the image enhancer."""
        self.models = {}
        self.logger = logging.getLogger(__name__)
        
    def _load_model(self, model_name: str) -> Optional[RealESRGANer]:
        """Load an AI model for image enhancement."""
        if not REALESRGAN_AVAILABLE:
            return None
            
        if model_name in self.models:
            return self.models[model_name]
            
        try:
            if model_name not in config.MODELS:
                raise ValueError(f"Unknown model: {model_name}")
                
            model_info = config.MODELS[model_name]
            
            # Initialize the model
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=model_info["scale"])
            
            # Create Real-ESRGAN upsampler
            upsampler = RealESRGANer(
                scale=model_info["scale"],
                model_path=None,  # Will use default pre-trained weights
                dni_weight=None,
                model=model,
                tile=0,
                tile_pad=10,
                pre_pad=0,
                half=False,
                gpu_id=None
            )
            
            self.models[model_name] = upsampler
            return upsampler
            
        except Exception as e:
            self.logger.error(f"Failed to load model {model_name}: {e}")
            return None
    
    def _basic_upscale(self, image: np.ndarray, scale_factor: int) -> np.ndarray:
        """Basic upscaling using OpenCV when AI models are not available."""
        height, width = image.shape[:2]
        new_height, new_width = height * scale_factor, width * scale_factor
        
        # Use INTER_CUBIC for better quality upscaling
        upscaled = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # Apply some basic enhancement
        # Sharpen the image slightly
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(upscaled, -1, kernel)
        
        # Blend original and sharpened (50% each for subtle effect)
        enhanced = cv2.addWeighted(upscaled, 0.7, sharpened, 0.3, 0)
        
        return enhanced
    
    def _denoise_image(self, image: np.ndarray) -> np.ndarray:
        """Apply denoising to the image."""
        # Use Non-Local Means Denoising
        if len(image.shape) == 3:
            # Color image
            denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        else:
            # Grayscale image
            denoised = cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
        return denoised
    
    def _enhance_colors(self, image: np.ndarray) -> np.ndarray:
        """Enhance colors and contrast."""
        # Convert to LAB color space for better color enhancement
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Split channels
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels and convert back to BGR
        enhanced_lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def enhance_image(self, input_path: Path, output_path: Path, 
                     model_name: str = "esrgan", scale_factor: int = 2) -> Path:
        """
        Enhance an image using AI models.
        
        Args:
            input_path: Path to input image
            output_path: Path to save enhanced image
            model_name: Name of the AI model to use
            scale_factor: Upscaling factor
            
        Returns:
            Path to the enhanced image
        """
        self.logger.info(f"Enhancing image: {input_path}")
        
        # Load image
        image = cv2.imread(str(input_path))
        if image is None:
            raise ValueError(f"Could not load image: {input_path}")
        
        # Check image size
        height, width = image.shape[:2]
        max_dim = max(height, width)
        if max_dim > config.MAX_IMAGE_SIZE:
            # Resize image to fit within limits
            scale = config.MAX_IMAGE_SIZE / max_dim
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            self.logger.info(f"Resized image to {new_width}x{new_height}")
        
        # Try to use AI model first
        model = self._load_model(model_name)
        if model and REALESRGAN_AVAILABLE:
            try:
                # Convert BGR to RGB for Real-ESRGAN
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Enhance using AI model
                enhanced_rgb, _ = model.enhance(rgb_image, outscale=scale_factor)
                
                # Convert back to BGR
                enhanced = cv2.cvtColor(enhanced_rgb, cv2.COLOR_RGB2BGR)
                
                self.logger.info(f"Enhanced using {model_name} model")
                
            except Exception as e:
                self.logger.warning(f"AI model enhancement failed: {e}. Using basic methods.")
                enhanced = self._basic_upscale(image, scale_factor)
        else:
            # Fallback to basic enhancement
            enhanced = self._basic_upscale(image, scale_factor)
            self.logger.info("Enhanced using basic upscaling")
        
        # Apply additional enhancements
        enhanced = self._denoise_image(enhanced)
        enhanced = self._enhance_colors(enhanced)
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save enhanced image
        success = cv2.imwrite(str(output_path), enhanced)
        if not success:
            raise RuntimeError(f"Failed to save enhanced image to: {output_path}")
        
        self.logger.info(f"Enhanced image saved to: {output_path}")
        return output_path