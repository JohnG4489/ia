#!/usr/bin/env python3
"""
AI Photo and Video Remastering Tool
Main entry point for the application.
"""

import click
import sys
from pathlib import Path
import config

# Import enhancer classes only when needed to avoid import errors
def get_image_enhancer():
    from src.image_enhancer import ImageEnhancer
    return ImageEnhancer()

def get_video_enhancer():
    from src.video_enhancer import VideoEnhancer
    return VideoEnhancer()

def get_web_app():
    from src.web_interface import create_app
    return create_app()

@click.group()
def cli():
    """AI Photo and Video Remastering Tool"""
    pass

@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output path')
@click.option('--model', '-m', default='esrgan', help='Enhancement model to use')
@click.option('--scale', '-s', default=2, type=int, help='Upscaling factor')
def enhance_image(input_path, output, model, scale):
    """Enhance a single image using AI."""
    input_file = Path(input_path)
    
    if input_file.suffix.lower() not in config.SUPPORTED_IMAGE_FORMATS:
        click.echo(f"Error: Unsupported image format {input_file.suffix}")
        sys.exit(1)
    
    if output is None:
        output = config.OUTPUT_DIR / f"{input_file.stem}_enhanced{input_file.suffix}"
    
    enhancer = get_image_enhancer()
    
    try:
        click.echo(f"Enhancing {input_path} with {model} model...")
        result_path = enhancer.enhance_image(input_file, Path(output), model, scale)
        click.echo(f"Enhanced image saved to: {result_path}")
    except Exception as e:
        click.echo(f"Error enhancing image: {e}")
        sys.exit(1)

@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output path')
@click.option('--model', '-m', default='esrgan', help='Enhancement model to use')
def enhance_video(input_path, output, model):
    """Enhance a video using AI frame-by-frame processing."""
    input_file = Path(input_path)
    
    if input_file.suffix.lower() not in config.SUPPORTED_VIDEO_FORMATS:
        click.echo(f"Error: Unsupported video format {input_file.suffix}")
        sys.exit(1)
    
    if output is None:
        output = config.OUTPUT_DIR / f"{input_file.stem}_enhanced{input_file.suffix}"
    
    enhancer = get_video_enhancer()
    
    try:
        click.echo(f"Enhancing video {input_path} with {model} model...")
        result_path = enhancer.enhance_video(input_file, Path(output), model)
        click.echo(f"Enhanced video saved to: {result_path}")
    except Exception as e:
        click.echo(f"Error enhancing video: {e}")
        sys.exit(1)

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--model', '-m', default='esrgan', help='Enhancement model to use')
@click.option('--scale', '-s', default=2, type=int, help='Upscaling factor')
def batch_enhance(input_dir, output, model, scale):
    """Batch enhance all images and videos in a directory."""
    input_path = Path(input_dir)
    
    if output is None:
        output = config.OUTPUT_DIR
    else:
        output = Path(output)
    
    output.mkdir(parents=True, exist_ok=True)
    
    # Find all supported media files
    media_files = []
    for ext in config.SUPPORTED_IMAGE_FORMATS | config.SUPPORTED_VIDEO_FORMATS:
        media_files.extend(input_path.glob(f"*{ext}"))
        media_files.extend(input_path.glob(f"*{ext.upper()}"))
    
    if not media_files:
        click.echo("No supported media files found in the input directory.")
        return
    
    click.echo(f"Found {len(media_files)} media files to process...")
    
    image_enhancer = get_image_enhancer()
    video_enhancer = get_video_enhancer()
    
    for file_path in media_files:
        try:
            output_file = output / f"{file_path.stem}_enhanced{file_path.suffix}"
            
            if file_path.suffix.lower() in config.SUPPORTED_IMAGE_FORMATS:
                click.echo(f"Processing image: {file_path.name}")
                image_enhancer.enhance_image(file_path, output_file, model, scale)
            else:
                click.echo(f"Processing video: {file_path.name}")
                video_enhancer.enhance_video(file_path, output_file, model)
                
        except Exception as e:
            click.echo(f"Error processing {file_path.name}: {e}")
            continue

@cli.command()
@click.option('--host', default=config.WEB_HOST, help='Host address')
@click.option('--port', default=config.WEB_PORT, help='Port number')
@click.option('--debug', default=config.WEB_DEBUG, help='Debug mode')
def web(host, port, debug):
    """Start the web interface."""
    app = get_web_app()
    click.echo(f"Starting web interface at http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    # Create necessary directories
    config.INPUT_DIR.mkdir(exist_ok=True)
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    config.MODELS_DIR.mkdir(exist_ok=True)
    config.UPLOAD_FOLDER.mkdir(exist_ok=True)
    
    cli()