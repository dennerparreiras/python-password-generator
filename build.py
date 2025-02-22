import os
import sys
import PyInstaller.__main__

def build_executable():
    """Build the executable with custom icon"""
    
    icon_path = os.path.abspath("password_icon.ico")
    
    if not os.path.exists(icon_path):
        print(f"Warning: Icon file not found at {icon_path}")
        return
    
    # PyInstaller command line arguments
    args = [
        'password_generator.py',
        '--onefile',
        '--windowed',
        '--clean',
        '--icon', icon_path,
        '--name', 'Password Generator',
        # Ensure icon is included in the bundle
        '--add-binary', f"{icon_path};." if sys.platform.startswith('win') else f"{icon_path}:.",
    ]
    
    # Add version file if available
    version_file = "version.txt"
    if os.path.exists(version_file):
        args.extend(['--version-file', version_file])
    
    print(f"Building with icon: {icon_path}")
    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    build_executable() 