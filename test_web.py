#!/usr/bin/env python3
"""
Test script for web interface functionality.
"""

import sys
from pathlib import Path
import tempfile

# Mock heavy dependencies that aren't available
class MockCV2:
    def imread(self, path): return None
    def imwrite(self, path, img): return True

class MockImageEnhancer:
    def enhance_image(self, input_path, output_path, model, scale):
        # Create a dummy output file for testing
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("Mock enhanced image")
        return output_path

class MockVideoEnhancer:
    def enhance_video(self, input_path, output_path, model, scale=2):
        # Create a dummy output file for testing
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("Mock enhanced video")
        return output_path

# Patch modules before importing
sys.modules['cv2'] = MockCV2()
sys.modules['realesrgan'] = type('module', (), {'RealESRGANer': None})()
sys.modules['basicsr'] = type('module', (), {'archs': type('module', (), {'rrdbnet_arch': type('module', (), {'RRDBNet': None})()})()})()

# Patch classes in the enhancer modules
import src.image_enhancer
import src.video_enhancer

src.image_enhancer.ImageEnhancer = MockImageEnhancer
src.video_enhancer.VideoEnhancer = MockVideoEnhancer

def test_web_interface():
    """Test web interface creation and routes."""
    print("=== Web Interface Test ===")
    
    try:
        from src.web_interface import create_app
        import config
        
        # Create Flask app
        app = create_app()
        app.config['TESTING'] = True
        
        print("  ✓ Flask app created successfully")
        
        # Test app creation
        with app.test_client() as client:
            # Test main page
            response = client.get('/')
            assert response.status_code == 200
            print("  ✓ Main page loads")
            
            # Test jobs page
            response = client.get('/jobs')
            assert response.status_code == 200
            print("  ✓ Jobs page loads")
            
            # Test API models endpoint
            response = client.get('/api/models')
            assert response.status_code == 200
            data = response.get_json()
            assert 'esrgan' in data
            print("  ✓ Models API works")
            
        return True
        
    except Exception as e:
        print(f"  ✗ Web interface test failed: {e}")
        return False

def test_cli_help():
    """Test CLI help functionality."""
    print("\n=== CLI Help Test ===")
    
    try:
        # Patch the enhancer imports in main.py
        import main
        main.ImageEnhancer = MockImageEnhancer
        main.VideoEnhancer = MockVideoEnhancer
        
        # Test CLI help
        from click.testing import CliRunner
        runner = CliRunner()
        
        result = runner.invoke(main.cli, ['--help'])
        assert result.exit_code == 0
        assert 'enhance-image' in result.output
        assert 'enhance-video' in result.output
        assert 'batch-enhance' in result.output
        assert 'web' in result.output
        
        print("  ✓ CLI help displays correctly")
        print("  ✓ All expected commands found")
        
        return True
        
    except Exception as e:
        print(f"  ✗ CLI help test failed: {e}")
        return False

def test_config_values():
    """Test configuration values."""
    print("\n=== Configuration Test ===")
    
    try:
        import config
        
        # Test that config has expected values
        assert hasattr(config, 'SUPPORTED_IMAGE_FORMATS')
        assert hasattr(config, 'SUPPORTED_VIDEO_FORMATS')
        assert hasattr(config, 'MODELS')
        assert hasattr(config, 'BASE_DIR')
        
        # Test model configuration
        assert 'esrgan' in config.MODELS
        assert 'description' in config.MODELS['esrgan']
        
        print("  ✓ Config attributes present")
        print("  ✓ Model configuration valid")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Configuration test failed: {e}")
        return False

def test_templates():
    """Test that templates exist and are valid."""
    print("\n=== Templates Test ===")
    
    try:
        templates_dir = Path(__file__).parent / 'templates'
        
        expected_templates = [
            'base.html',
            'index.html',
            'job_status.html',
            'jobs.html'
        ]
        
        for template in expected_templates:
            template_path = templates_dir / template
            assert template_path.exists(), f"Template {template} not found"
            
            content = template_path.read_text()
            assert len(content) > 0, f"Template {template} is empty"
            
            print(f"  ✓ Template {template} exists and has content")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Templates test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("AI Photo & Video Remastering - Web Interface Tests")
    print("=" * 55)
    
    tests = [
        test_config_values,
        test_templates,
        test_cli_help,
        test_web_interface,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 55)
    print("Test Results:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "PASS" if result else "FAIL"
        print(f"  {test.__name__}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All web interface tests passed!")
        print("\nThe application is ready to run:")
        print("1. Install full dependencies: pip install -r requirements.txt")
        print("2. Start web interface: python main.py web")
        print("3. Visit: http://localhost:5000")
        return True
    else:
        print("✗ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)