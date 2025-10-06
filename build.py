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
    """Create a GUI launcher that lets users choose game mode."""
    launcher_code = '''#!/usr/bin/env python3
"""
Tetris LAN Multiplayer - GUI Launcher
Allows users to choose game mode without using terminal.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os


class TetrisLauncher:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tetris LAN Multiplayer")
        self.window.geometry("450x400")
        self.window.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = tk.Label(
            self.window,
            text="TETRIS LAN MULTIPLAYER",
            font=("Arial", 18, "bold"),
            fg="#00FFFF"
        )
        title.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(
            self.window,
            text="Choose Game Mode",
            font=("Arial", 12)
        )
        subtitle.pack(pady=5)
        
        # Frame for buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Single Player Button
        single_btn = tk.Button(
            button_frame,
            text="🎮 Single Player",
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=15,
            command=self.launch_single,
            cursor="hand2"
        )
        single_btn.pack(fill='x', pady=10)
        
        # Host Game Button
        host_btn = tk.Button(
            button_frame,
            text="🖥️  Host LAN Game",
            font=("Arial", 14),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=15,
            command=self.launch_host,
            cursor="hand2"
        )
        host_btn.pack(fill='x', pady=10)
        
        # Join Game Button
        join_btn = tk.Button(
            button_frame,
            text="🔌 Join LAN Game",
            font=("Arial", 14),
            bg="#FF9800",
            fg="white",
            padx=20,
            pady=15,
            command=self.launch_join,
            cursor="hand2"
        )
        join_btn.pack(fill='x', pady=10)
        
        # Info text
        info = tk.Label(
            self.window,
            text="TETR.IO Format • Next 2 Pieces Preview",
            font=("Arial", 9),
            fg="gray"
        )
        info.pack(pady=10)
        
    def launch_single(self):
        """Launch single player mode."""
        self.window.destroy()
        subprocess.run([sys.executable, 'main.py', '--mode', 'single'])
        
    def launch_host(self):
        """Launch host mode with port selection."""
        port = self.ask_port()
        if port:
            self.window.destroy()
            subprocess.run([sys.executable, 'main.py', '--mode', 'host', '--port', str(port)])
    
    def launch_join(self):
        """Launch join mode with host/port input."""
        dialog = JoinDialog(self.window)
        self.window.wait_window(dialog.dialog)
        
        if dialog.result:
            host, port = dialog.result
            self.window.destroy()
            subprocess.run([sys.executable, 'main.py', '--mode', 'join', '--host', host, '--port', str(port)])
    
    def ask_port(self):
        """Ask user for port number."""
        dialog = tk.Toplevel(self.window)
        dialog.title("Host Game")
        dialog.geometry("300x150")
        dialog.transient(self.window)
        dialog.grab_set()
        
        tk.Label(dialog, text="Enter Port Number:", font=("Arial", 11)).pack(pady=10)
        
        port_var = tk.StringVar(value="5555")
        port_entry = ttk.Entry(dialog, textvariable=port_var, font=("Arial", 12), width=15)
        port_entry.pack(pady=5)
        port_entry.select_range(0, tk.END)
        port_entry.focus()
        
        result = [None]
        
        def on_ok():
            try:
                port = int(port_var.get())
                if 1024 <= port <= 65535:
                    result[0] = port
                    dialog.destroy()
                else:
                    messagebox.showerror("Invalid Port", "Port must be between 1024 and 65535")
            except ValueError:
                messagebox.showerror("Invalid Port", "Please enter a valid number")
        
        def on_cancel():
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text="Start", command=on_ok).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=on_cancel).pack(side='left', padx=5)
        
        port_entry.bind('<Return>', lambda e: on_ok())
        
        self.window.wait_window(dialog)
        return result[0]
    
    def run(self):
        self.window.mainloop()


class JoinDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Join Game")
        self.dialog.geometry("350x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.result = None
        
        tk.Label(self.dialog, text="Join LAN Game", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Host input
        frame1 = ttk.Frame(self.dialog)
        frame1.pack(pady=5, padx=20, fill='x')
        tk.Label(frame1, text="Host IP:", width=10, anchor='w').pack(side='left')
        self.host_var = tk.StringVar(value="192.168.1.100")
        host_entry = ttk.Entry(frame1, textvariable=self.host_var, width=20)
        host_entry.pack(side='left', padx=5)
        
        # Port input
        frame2 = ttk.Frame(self.dialog)
        frame2.pack(pady=5, padx=20, fill='x')
        tk.Label(frame2, text="Port:", width=10, anchor='w').pack(side='left')
        self.port_var = tk.StringVar(value="5555")
        port_entry = ttk.Entry(frame2, textvariable=self.port_var, width=20)
        port_entry.pack(side='left', padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Connect", command=self.on_ok).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.on_cancel).pack(side='left', padx=5)
        
        host_entry.focus()
        host_entry.select_range(0, tk.END)
    
    def on_ok(self):
        try:
            host = self.host_var.get().strip()
            port = int(self.port_var.get())
            
            if not host:
                messagebox.showerror("Invalid Input", "Please enter a host IP address")
                return
            
            if not (1024 <= port <= 65535):
                messagebox.showerror("Invalid Port", "Port must be between 1024 and 65535")
                return
            
            self.result = (host, port)
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Invalid Port", "Please enter a valid port number")
    
    def on_cancel(self):
        self.dialog.destroy()


if __name__ == '__main__':
    launcher = TetrisLauncher()
    launcher.run()
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
        '--onefile',
        '--windowed',
        '--name', 'Tetris_Launcher',
        '--add-data', f'game_logic{os.pathsep}game_logic',
        '--add-data', f'rendering{os.pathsep}rendering',
        '--add-data', f'networking{os.pathsep}networking',
        '--hidden-import', 'pygame',
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

