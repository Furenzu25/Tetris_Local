#!/usr/bin/env python3
"""
Build script to package Tetris game into standalone executables.
Creates executables for Windows, macOS, and Linux.
"""

import os
import sys
import platform
import subprocess
import shutil


def get_platform():
    """Get the current platform."""
    system = platform.system().lower()
    if system == 'darwin':
        return 'macos'
    return system


def clean_build_folders():
    """Clean up previous build artifacts."""
    print("Cleaning build folders...")
    folders = ['build', 'dist', '__pycache__']
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  ✓ Removed {folder}/")
    
    # Remove spec files
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            os.remove(file)
            print(f"  ✓ Removed {file}")


def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '-r', 'requirements-dev.txt'])
    print("  ✓ Dependencies installed")


def build_executable(mode, icon_path=None):
    """
    Build executable for specific game mode.
    
    Args:
        mode (str): Game mode ('single', 'host', 'join')
        icon_path (str): Path to icon file (optional)
    """
    print(f"\nBuilding Tetris_{mode.capitalize()}.exe...")
    
    # Determine output name based on platform
    plat = get_platform()
    if plat == 'windows':
        ext = '.exe'
    elif plat == 'macos':
        ext = '.app'
    else:
        ext = ''
    
    output_name = f'Tetris_{mode.capitalize()}'
    
    # Build PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',  # Single executable
        '--windowed',  # No console window
        '--name', output_name,
        '--add-data', f'game_logic{os.pathsep}game_logic',
        '--add-data', f'rendering{os.pathsep}rendering',
        '--add-data', f'networking{os.pathsep}networking',
        '--hidden-import', 'pygame',
        '--hidden-import', 'game_logic',
        '--hidden-import', 'rendering',
        '--hidden-import', 'networking',
    ]
    
    # Add icon if provided
    if icon_path and os.path.exists(icon_path):
        cmd.extend(['--icon', icon_path])
    
    # Add mode-specific arguments
    if mode == 'single':
        cmd.extend(['--', '--mode', 'single'])
    elif mode == 'host':
        cmd.extend(['--', '--mode', 'host'])
    # For join mode, we'll need a GUI launcher
    
    cmd.append('main.py')
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  ✓ Built {output_name}{ext}")
        return True
    else:
        print(f"  ✗ Build failed for {mode}")
        print(result.stderr)
        return False


def create_launcher_gui():
    """Create a simple launcher that goes straight to single player."""
    launcher_code = '''#!/usr/bin/env python3
"""
Simple Tetris Launcher - Single Player Mode
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        print("Starting Tetris Single Player...")
        
        # Import and run single player game
        from game_controller import GameController
        
        print("✓ Game loaded successfully!")
        print("Controls:")
        print("  Arrow Keys: Move piece")
        print("  Up/X: Rotate clockwise")
        print("  Z: Rotate counter-clockwise")
        print("  Space: Hard drop")
        print("  Left Shift: Hold piece")
        print("  ESC: Pause")
        print("  R: Restart (when game over)")
        print()
        
        # Create controller for single player
        controller = GameController(mode='single')
        
        # Run the game
        controller.run()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()
'''
    
    with open('launcher.py', 'w') as f:
        f.write(launcher_code)
    
    print("  ✓ Created launcher.py")


def build_all():
    """Build all executables."""
    print("=" * 60)
    print("  TETRIS LAN MULTIPLAYER - BUILD SCRIPT")
    print("=" * 60)
    
    # Clean previous builds
    clean_build_folders()
    
    # Install dependencies
    install_dependencies()
    
    # Create GUI launcher
    create_launcher_gui()
    
    # Build main launcher
    print("\nBuilding Tetris_Launcher...")
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onedir',  # Changed from --onefile to fix macOS issues
        '--windowed',
        '--name', 'Tetris_Launcher',
        '--add-data', f'game_logic{os.pathsep}game_logic',
        '--add-data', f'rendering{os.pathsep}rendering',
        '--add-data', f'networking{os.pathsep}networking',
        '--hidden-import', 'pygame',
        '--hidden-import', 'game_logic',
        '--hidden-import', 'rendering',
        '--hidden-import', 'networking',
        '--hidden-import', 'game_logic.pieces',
        '--hidden-import', 'game_logic.board',
        '--hidden-import', 'game_logic.game_engine',
        '--hidden-import', 'rendering.renderer',
        '--hidden-import', 'networking.protocol',
        '--hidden-import', 'networking.server',
        '--hidden-import', 'networking.client',
        'launcher.py'
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("  ✓ BUILD SUCCESSFUL!")
        print("=" * 60)
        print(f"\nExecutable created in: dist/")
        print(f"Look for: Tetris_Launcher{'.exe' if get_platform() == 'windows' else ''}")
        print("\nDistribute this file to your friends - no Python needed!")
        return True
    else:
        print("\n✗ Build failed")
        return False


if __name__ == '__main__':
    success = build_all()
    sys.exit(0 if success else 1)

