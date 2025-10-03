"""Web interface for AI photo and video remastering."""

from flask import Flask, render_template, request, flash, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import threading
import time
from datetime import datetime
import uuid
import logging

from .image_enhancer import ImageEnhancer
from .video_enhancer import VideoEnhancer
import config

# Global variables for tracking jobs
active_jobs = {}
completed_jobs = {}

def create_app():
    """Create Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ai-remastering-secret-key'
    app.config['UPLOAD_FOLDER'] = str(config.UPLOAD_FOLDER)
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    
    # Ensure upload folder exists
    config.UPLOAD_FOLDER.mkdir(exist_ok=True)
    
    def allowed_file(filename):
        """Check if file type is allowed."""
        if '.' not in filename:
            return False
        ext = '.' + filename.rsplit('.', 1)[1].lower()
        return ext in (config.SUPPORTED_IMAGE_FORMATS | config.SUPPORTED_VIDEO_FORMATS)
    
    def process_file_async(job_id, input_path, output_path, file_type, model, scale_factor):
        """Process file in background thread."""
        try:
            active_jobs[job_id]['status'] = 'processing'
            active_jobs[job_id]['progress'] = 0
            
            if file_type == 'image':
                enhancer = ImageEnhancer()
                result_path = enhancer.enhance_image(input_path, output_path, model, scale_factor)
            else:  # video
                enhancer = VideoEnhancer()
                result_path = enhancer.enhance_video(input_path, output_path, model, scale_factor)
            
            # Move to completed jobs
            completed_jobs[job_id] = {
                'input_path': str(input_path),
                'output_path': str(result_path),
                'file_type': file_type,
                'model': model,
                'scale_factor': scale_factor,
                'completed_at': datetime.now(),
                'status': 'completed'
            }
            
            # Remove from active jobs
            if job_id in active_jobs:
                del active_jobs[job_id]
                
        except Exception as e:
            # Move to completed jobs with error status
            completed_jobs[job_id] = {
                'status': 'error',
                'error': str(e),
                'completed_at': datetime.now()
            }
            
            if job_id in active_jobs:
                del active_jobs[job_id]
    
    @app.route('/')
    def index():
        """Main page."""
        return render_template('index.html', models=config.MODELS)
    
    @app.route('/upload', methods=['POST'])
    def upload_file():
        """Handle file upload and start processing."""
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if not allowed_file(file.filename):
            flash('File type not supported')
            return redirect(request.url)
        
        # Get form parameters
        model = request.form.get('model', 'esrgan')
        scale_factor = int(request.form.get('scale_factor', 2))
        
        if model not in config.MODELS:
            flash('Invalid model selected')
            return redirect(request.url)
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{filename}"
        
        input_path = config.UPLOAD_FOLDER / safe_filename
        file.save(str(input_path))
        
        # Determine file type
        ext = '.' + filename.rsplit('.', 1)[1].lower()
        file_type = 'image' if ext in config.SUPPORTED_IMAGE_FORMATS else 'video'
        
        # Generate output path
        output_filename = f"{timestamp}_{Path(filename).stem}_enhanced{ext}"
        output_path = config.OUTPUT_DIR / output_filename
        
        # Create job ID
        job_id = str(uuid.uuid4())
        
        # Start processing in background
        active_jobs[job_id] = {
            'filename': filename,
            'file_type': file_type,
            'model': model,
            'scale_factor': scale_factor,
            'status': 'queued',
            'progress': 0,
            'started_at': datetime.now()
        }
        
        thread = threading.Thread(
            target=process_file_async,
            args=(job_id, input_path, output_path, file_type, model, scale_factor)
        )
        thread.daemon = True
        thread.start()
        
        flash(f'Processing started for {filename}')
        return redirect(url_for('job_status', job_id=job_id))
    
    @app.route('/job/<job_id>')
    def job_status(job_id):
        """Show job status page."""
        job = active_jobs.get(job_id) or completed_jobs.get(job_id)
        
        if not job:
            flash('Job not found')
            return redirect(url_for('index'))
        
        return render_template('job_status.html', job=job, job_id=job_id)
    
    @app.route('/api/job/<job_id>/status')
    def api_job_status(job_id):
        """API endpoint for job status."""
        job = active_jobs.get(job_id) or completed_jobs.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify(job)
    
    @app.route('/download/<job_id>')
    def download_file(job_id):
        """Download processed file."""
        job = completed_jobs.get(job_id)
        
        if not job or job['status'] != 'completed':
            flash('File not ready for download')
            return redirect(url_for('index'))
        
        output_path = Path(job['output_path'])
        if not output_path.exists():
            flash('Output file not found')
            return redirect(url_for('index'))
        
        return send_file(
            str(output_path),
            as_attachment=True,
            download_name=output_path.name
        )
    
    @app.route('/jobs')
    def list_jobs():
        """List all jobs."""
        all_jobs = {}
        
        # Add active jobs
        for job_id, job in active_jobs.items():
            all_jobs[job_id] = {**job, 'id': job_id}
        
        # Add completed jobs
        for job_id, job in completed_jobs.items():
            all_jobs[job_id] = {**job, 'id': job_id}
        
        # Sort by start time (most recent first)
        sorted_jobs = sorted(
            all_jobs.values(),
            key=lambda x: x.get('started_at', x.get('completed_at', datetime.min)),
            reverse=True
        )
        
        return render_template('jobs.html', jobs=sorted_jobs)
    
    @app.route('/api/models')
    def api_models():
        """API endpoint for available models."""
        return jsonify(config.MODELS)
    
    return app

# HTML Templates (inline for simplicity)
def create_templates():
    """Create template files."""
    templates_dir = Path(__file__).parent.parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # Base template
    base_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}AI Photo & Video Remastering{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .upload-area {
            border: 2px dashed #ccc;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
        }
        .upload-area:hover {
            border-color: #007bff;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">AI Remastering</a>
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('index') }}">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('list_jobs') }}">Jobs</a>
                </li>
            </ul>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-info alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
    
    (templates_dir / 'base.html').write_text(base_template)
    
    # Index template
    index_template = '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-md-8 offset-md-2">
        <h1 class="text-center mb-4">AI Photo & Video Remastering</h1>
        <p class="text-center text-muted">Upload photos and videos to enhance them using AI models</p>
        
        <form method="POST" action="{{ url_for('upload_file') }}" enctype="multipart/form-data">
            <div class="upload-area">
                <input type="file" class="form-control" name="file" accept=".jpg,.jpeg,.png,.bmp,.tiff,.webp,.mp4,.avi,.mov,.mkv,.wmv" required>
                <div class="mt-2">
                    <small class="text-muted">Supported formats: Images (JPG, PNG, BMP, TIFF, WebP) and Videos (MP4, AVI, MOV, MKV, WMV)</small>
                </div>
            </div>
            
            <div class="row mb-3">
                <div class="col-md-6">
                    <label for="model" class="form-label">AI Model:</label>
                    <select class="form-select" name="model" id="model">
                        {% for model_key, model_info in models.items() %}
                        <option value="{{ model_key }}" {% if model_key == 'esrgan' %}selected{% endif %}>
                            {{ model_info.description }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-6">
                    <label for="scale_factor" class="form-label">Scale Factor:</label>
                    <select class="form-select" name="scale_factor" id="scale_factor">
                        <option value="2" selected>2x (Recommended)</option>
                        <option value="4">4x (Slower, Higher Quality)</option>
                    </select>
                </div>
            </div>
            
            <button type="submit" class="btn btn-primary btn-lg w-100">Start Enhancement</button>
        </form>
    </div>
</div>
{% endblock %}'''
    
    (templates_dir / 'index.html').write_text(index_template)

if __name__ == '__main__':
    create_templates()
    app = create_app()
    app.run(debug=True)