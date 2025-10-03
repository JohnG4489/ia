"""Video enhancement module using AI models."""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
import logging
from tqdm import tqdm
import tempfile
import os

from .image_enhancer import ImageEnhancer
import config

class VideoEnhancer:
    """AI-powered video enhancement class."""
    
    def __init__(self):
        """Initialize the video enhancer."""
        self.image_enhancer = ImageEnhancer()
        self.logger = logging.getLogger(__name__)
        
    def _get_video_info(self, video_path: Path) -> dict:
        """Extract video information."""
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        info = {
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fourcc': int(cap.get(cv2.CAP_PROP_FOURCC))
        }
        
        cap.release()
        return info
    
    def _stabilize_frame(self, frame: np.ndarray, prev_frame: Optional[np.ndarray] = None) -> np.ndarray:
        """Apply basic video stabilization to a frame."""
        if prev_frame is None:
            return frame
            
        # Convert to grayscale for motion estimation
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        
        # Detect features in previous frame
        detector = cv2.goodFeaturesToTrack(prev_gray, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
        
        if detector is None or len(detector) < 10:
            return frame
            
        # Calculate optical flow
        lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
        try:
            new_features, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, detector, None, **lk_params)
            
            # Filter good points
            good_new = new_features[status == 1]
            good_old = detector[status == 1]
            
            if len(good_new) < 10:
                return frame
                
            # Find transformation matrix
            transform = cv2.estimateAffinePartial2D(good_old, good_new)[0]
            
            if transform is not None:
                # Apply stabilization transform
                height, width = frame.shape[:2]
                stabilized = cv2.warpAffine(frame, transform, (width, height))
                return stabilized
                
        except Exception as e:
            self.logger.warning(f"Stabilization failed: {e}")
            
        return frame
    
    def _enhance_frame(self, frame: np.ndarray, model_name: str, scale_factor: int = 2) -> np.ndarray:
        """Enhance a single video frame."""
        # Create temporary file for frame processing
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_input:
            temp_input_path = Path(temp_input.name)
            
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_output:
            temp_output_path = Path(temp_output.name)
        
        try:
            # Save frame to temporary file
            cv2.imwrite(str(temp_input_path), frame)
            
            # Enhance using image enhancer
            self.image_enhancer.enhance_image(temp_input_path, temp_output_path, model_name, scale_factor)
            
            # Load enhanced frame
            enhanced_frame = cv2.imread(str(temp_output_path))
            
            if enhanced_frame is None:
                self.logger.warning("Frame enhancement failed, using original frame")
                return frame
                
            return enhanced_frame
            
        finally:
            # Clean up temporary files
            try:
                temp_input_path.unlink()
                temp_output_path.unlink()
            except Exception:
                pass
    
    def enhance_video(self, input_path: Path, output_path: Path, 
                     model_name: str = "esrgan", scale_factor: int = 2,
                     stabilize: bool = True) -> Path:
        """
        Enhance a video using AI models frame by frame.
        
        Args:
            input_path: Path to input video
            output_path: Path to save enhanced video
            model_name: Name of the AI model to use
            scale_factor: Upscaling factor
            stabilize: Whether to apply video stabilization
            
        Returns:
            Path to the enhanced video
        """
        self.logger.info(f"Enhancing video: {input_path}")
        
        # Get video information
        video_info = self._get_video_info(input_path)
        self.logger.info(f"Video info: {video_info}")
        
        # Open input video
        cap = cv2.VideoCapture(str(input_path))
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {input_path}")
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Set up video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        enhanced_width = video_info['width'] * scale_factor
        enhanced_height = video_info['height'] * scale_factor
        
        out = cv2.VideoWriter(
            str(output_path),
            fourcc,
            video_info['fps'],
            (enhanced_width, enhanced_height)
        )
        
        if not out.isOpened():
            cap.release()
            raise RuntimeError(f"Could not open output video writer: {output_path}")
        
        frame_count = 0
        prev_frame = None
        
        # Process frames with progress bar
        with tqdm(total=video_info['frame_count'], desc="Processing frames") as pbar:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                try:
                    # Apply stabilization if requested
                    if stabilize and prev_frame is not None:
                        frame = self._stabilize_frame(frame, prev_frame)
                    
                    # Enhance frame
                    enhanced_frame = self._enhance_frame(frame, model_name, scale_factor)
                    
                    # Write enhanced frame
                    out.write(enhanced_frame)
                    
                    prev_frame = frame.copy()
                    frame_count += 1
                    pbar.update(1)
                    
                except Exception as e:
                    self.logger.error(f"Error processing frame {frame_count}: {e}")
                    # Write original frame if enhancement fails
                    resized_frame = cv2.resize(frame, (enhanced_width, enhanced_height), interpolation=cv2.INTER_CUBIC)
                    out.write(resized_frame)
                    frame_count += 1
                    pbar.update(1)
        
        # Release resources
        cap.release()
        out.release()
        
        self.logger.info(f"Processed {frame_count} frames")
        self.logger.info(f"Enhanced video saved to: {output_path}")
        
        return output_path
    
    def extract_frames(self, video_path: Path, output_dir: Path, 
                      frame_interval: int = 1) -> list:
        """
        Extract frames from a video for batch processing.
        
        Args:
            video_path: Path to input video
            output_dir: Directory to save extracted frames
            frame_interval: Extract every nth frame (1 = all frames)
            
        Returns:
            List of extracted frame paths
        """
        self.logger.info(f"Extracting frames from: {video_path}")
        
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        frame_paths = []
        frame_count = 0
        saved_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                frame_filename = f"frame_{saved_count:06d}.png"
                frame_path = output_dir / frame_filename
                cv2.imwrite(str(frame_path), frame)
                frame_paths.append(frame_path)
                saved_count += 1
            
            frame_count += 1
        
        cap.release()
        
        self.logger.info(f"Extracted {saved_count} frames from {frame_count} total frames")
        return frame_paths
    
    def create_video_from_frames(self, frame_dir: Path, output_path: Path, 
                               fps: float = 30.0) -> Path:
        """
        Create a video from enhanced frames.
        
        Args:
            frame_dir: Directory containing enhanced frames
            output_path: Path to save output video
            fps: Frames per second for output video
            
        Returns:
            Path to the created video
        """
        self.logger.info(f"Creating video from frames in: {frame_dir}")
        
        # Get all frame files
        frame_files = sorted([f for f in frame_dir.glob("*.png")])
        
        if not frame_files:
            raise ValueError(f"No frame files found in: {frame_dir}")
        
        # Read first frame to get dimensions
        first_frame = cv2.imread(str(frame_files[0]))
        if first_frame is None:
            raise ValueError(f"Could not read first frame: {frame_files[0]}")
        
        height, width = first_frame.shape[:2]
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Set up video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        if not out.isOpened():
            raise RuntimeError(f"Could not open output video writer: {output_path}")
        
        # Write frames to video
        with tqdm(frame_files, desc="Creating video") as pbar:
            for frame_file in pbar:
                frame = cv2.imread(str(frame_file))
                if frame is not None:
                    out.write(frame)
        
        out.release()
        
        self.logger.info(f"Created video: {output_path}")
        return output_path