#!/usr/bin/env python3
"""
Basic test script to verify the project structure without heavy dependencies.
"""

import sys
from pathlib import Path
import importlib.util

def test_project_structure():
    """Test that all expected files and directories exist."""
    base_dir = Path(__file__).parent
    
    expected_files = [
        "main.py",
        "config.py",
        "requirements.txt",
        "setup.py",
        "README.md",
        ".gitignore",
        "src/__init__.py",
        "src/image_enhancer.py",
        "src/video_enhancer.py",
        "src/web_interface.py",
        "examples/demo.py"
    ]
    
    print("=== Project Structure Test ===")
    
    all_good = True
    for file_path in expected_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            all_good = False
    
    return all_good

def test_basic_imports():
    """Test basic Python imports that don't require external dependencies."""
    print("\n=== Basic Imports Test ===")
    
    try:
        import config
        print("  ✓ config.py imports successfully")
        
        # Test config values
        assert hasattr(config, 'SUPPORTED_IMAGE_FORMATS')
        assert hasattr(config, 'SUPPORTED_VIDEO_FORMATS')
        assert hasattr(config, 'MODELS')
        print("  ✓ Config has expected attributes")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Basic imports failed: {e}")
        return False

def test_cli_structure():
    """Test that the main CLI structure is valid."""
    print("\n=== CLI Structure Test ===")
    
    try:
        # Read main.py content
        main_file = Path(__file__).parent / "main.py"
        content = main_file.read_text()
        
        # Check for expected CLI commands
        expected_commands = [
            "enhance_image",
            "enhance_video", 
            "batch_enhance",
            "web"
        ]
        
        all_found = True
        for command in expected_commands:
            if f"def {command}(" in content:
                print(f"  ✓ Command '{command}' found")
            else:
                print(f"  ✗ Command '{command}' missing")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"  ✗ CLI structure test failed: {e}")
        return False

def test_readme():
    """Test that README has expected content."""
    print("\n=== README Test ===")
    
    try:
        readme_file = Path(__file__).parent / "README.md"
        content = readme_file.read_text()
        
        expected_sections = [
            "AI Photo & Video Remastering",
            "Fonctionnalités",
            "Installation",
            "Utilisation",
            "Interface en ligne de commande",
            "Interface web"
        ]
        
        all_found = True
        for section in expected_sections:
            if section in content:
                print(f"  ✓ Section '{section}' found")
            else:
                print(f"  ✗ Section '{section}' missing")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"  ✗ README test failed: {e}")
        return False

def test_requirements():
    """Test that requirements.txt has expected dependencies."""
    print("\n=== Requirements Test ===")
    
    try:
        req_file = Path(__file__).parent / "requirements.txt"
        content = req_file.read_text()
        
        expected_deps = [
            "opencv-python",
            "Pillow",
            "numpy",
            "torch",
            "flask",
            "click",
            "realesrgan"
        ]
        
        all_found = True
        for dep in expected_deps:
            if dep in content:
                print(f"  ✓ Dependency '{dep}' found")
            else:
                print(f"  ✗ Dependency '{dep}' missing")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"  ✗ Requirements test failed: {e}")
        return False

def main():
    """Run all basic tests."""
    print("AI Photo & Video Remastering - Basic Tests")
    print("=" * 50)
    
    tests = [
        test_project_structure,
        test_basic_imports,
        test_cli_structure,
        test_readme,
        test_requirements
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("Test Results:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "PASS" if result else "FAIL"
        print(f"  {test.__name__}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All basic tests passed! Project structure is correct.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run demo: python examples/demo.py")
        print("3. Test CLI: python main.py --help")
        return True
    else:
        print("✗ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)