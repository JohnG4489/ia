#!/usr/bin/env python3
"""
Demo script showing basic usage of the AI remastering tools.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.image_enhancer import ImageEnhancer
from src.video_enhancer import VideoEnhancer
import config

def create_sample_image():
    """Create a simple sample image for testing."""
    try:
        import cv2
        import numpy as np
        
        # Create a simple test image
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Add some patterns
        cv2.rectangle(img, (10, 10), (50, 50), (255, 0, 0), -1)  # Blue rectangle
        cv2.circle(img, (75, 25), 15, (0, 255, 0), -1)  # Green circle
        cv2.line(img, (10, 70), (90, 90), (0, 0, 255), 2)  # Red line
        
        # Add some noise to make enhancement more visible
        noise = np.random.randint(0, 50, img.shape, dtype=np.uint8)
        img = cv2.add(img, noise)
        
        # Save sample image
        sample_path = config.INPUT_DIR / "sample.png"
        config.INPUT_DIR.mkdir(exist_ok=True)
        cv2.imwrite(str(sample_path), img)
        
        return sample_path
        
    except ImportError:
        print("OpenCV not available. Cannot create sample image.")
        return None

def demo_image_enhancement():
    """Demonstrate image enhancement."""
    print("=== Image Enhancement Demo ===")
    
    # Create or use existing sample image
    sample_image = create_sample_image()
    
    if sample_image is None:
        print("No sample image available. Skipping image demo.")
        return
    
    print(f"Using sample image: {sample_image}")
    
    # Create image enhancer
    enhancer = ImageEnhancer()
    
    # Enhance image
    output_path = config.OUTPUT_DIR / "sample_enhanced.png"
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    
    try:
        result = enhancer.enhance_image(
            input_path=sample_image,
            output_path=output_path,
            model_name="esrgan",
            scale_factor=2
        )
        
        print(f"Enhanced image saved to: {result}")
        print("Image enhancement completed successfully!")
        
    except Exception as e:
        print(f"Image enhancement failed: {e}")

def demo_batch_processing():
    """Demonstrate batch processing capabilities."""
    print("\n=== Batch Processing Demo ===")
    
    # Check if input directory has files
    input_files = []
    if config.INPUT_DIR.exists():
        for ext in config.SUPPORTED_IMAGE_FORMATS:
            input_files.extend(list(config.INPUT_DIR.glob(f"*{ext}")))
    
    if not input_files:
        print("No input files found for batch processing.")
        return
    
    print(f"Found {len(input_files)} files for batch processing")
    
    enhancer = ImageEnhancer()
    
    for input_file in input_files[:3]:  # Process max 3 files for demo
        try:
            output_file = config.OUTPUT_DIR / f"{input_file.stem}_batch_enhanced{input_file.suffix}"
            
            print(f"Processing: {input_file.name}")
            enhancer.enhance_image(input_file, output_file)
            print(f"Saved: {output_file.name}")
            
        except Exception as e:
            print(f"Failed to process {input_file.name}: {e}")

def print_system_info():
    """Print system information and available features."""
    print("=== System Information ===")
    print(f"Python version: {sys.version}")
    
    # Check dependencies
    dependencies = [
        ("OpenCV", "cv2"),
        ("PIL/Pillow", "PIL"),
        ("NumPy", "numpy"),
        ("Real-ESRGAN", "realesrgan"),
        ("PyTorch", "torch"),
        ("Flask", "flask"),
        ("Click", "click"),
    ]
    
    print("\nDependencies:")
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"  ✓ {name}: Available")
        except ImportError:
            print(f"  ✗ {name}: Not available")
    
    print(f"\nConfiguration:")
    print(f"  Input directory: {config.INPUT_DIR}")
    print(f"  Output directory: {config.OUTPUT_DIR}")
    print(f"  Models directory: {config.MODELS_DIR}")
    print(f"  Max image size: {config.MAX_IMAGE_SIZE}px")
    print(f"  Device: {config.DEVICE}")
    
    print(f"\nSupported formats:")
    print(f"  Images: {', '.join(sorted(config.SUPPORTED_IMAGE_FORMATS))}")
    print(f"  Videos: {', '.join(sorted(config.SUPPORTED_VIDEO_FORMATS))}")
    
    print(f"\nAvailable models:")
    for model_key, model_info in config.MODELS.items():
        try:
            print(f"  {model_key}: {model_info['description']}")
        except KeyError:
            print(f"  {model_key}: Model configuration error")

def main():
    """Main demo function."""
    print("AI Photo & Video Remastering - Demo")
    print("=" * 40)
    
    # Print system info
    print_system_info()
    
    # Create necessary directories
    config.INPUT_DIR.mkdir(exist_ok=True)
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    config.MODELS_DIR.mkdir(exist_ok=True)
    
    print("\n" + "=" * 40)
    
    # Run demos
    demo_image_enhancement()
    demo_batch_processing()
    
    print("\n" + "=" * 40)
    print("Demo completed!")
    print(f"Check the output directory: {config.OUTPUT_DIR}")
    
    print("\nNext steps:")
    print("1. Add your own images to the input/ directory")
    print("2. Run: python main.py enhance-image input/yourimage.jpg")
    print("3. Or start the web interface: python main.py web")

if __name__ == "__main__":
    main()