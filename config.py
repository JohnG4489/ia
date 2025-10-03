"""Configuration settings for AI photo and video remastering."""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
MODELS_DIR = BASE_DIR / "models"

# Supported file formats
SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
SUPPORTED_VIDEO_FORMATS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}

# Processing settings
DEFAULT_UPSCALE_FACTOR = 2
MAX_IMAGE_SIZE = 4096  # Maximum dimension for processing
BATCH_SIZE = 4
DEVICE = "cuda" if os.environ.get("CUDA_AVAILABLE") else "cpu"

# Model settings
MODELS = {
    "esrgan": {
        "name": "RealESRGAN_x4plus",
        "scale": 4,
        "description": "Real-ESRGAN 4x upscaling model"
    },
    "esrgan_anime": {
        "name": "RealESRGAN_x4plus_anime_6B",
        "scale": 4,
        "description": "Real-ESRGAN optimized for anime/artwork"
    }
}

# Web interface settings
WEB_HOST = "127.0.0.1"
WEB_PORT = 5000
WEB_DEBUG = True
UPLOAD_FOLDER = BASE_DIR / "uploads"
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size