"""Setup script for AI Photo and Video Remastering."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="ai-remastering",
    version="1.0.0",
    author="JohnG4489",
    description="AI-powered photo and video remastering tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.1",
        "Pillow>=10.0.1",
        "numpy>=1.24.3",
        "torch>=2.0.1",
        "torchvision>=0.15.2",
        "scipy>=1.11.2",
        "flask>=2.3.3",
        "werkzeug>=2.3.7",
        "click>=8.1.7",
        "tqdm>=4.66.1",
        "scikit-image>=0.21.0",
        "imageio>=2.31.3",
        "imageio-ffmpeg>=0.4.9",
        "realesrgan>=0.3.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-remaster=main:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)