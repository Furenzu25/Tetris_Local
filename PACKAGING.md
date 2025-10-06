# Packaging Tetris as Standalone Executable

This guide explains how to package the Tetris game into a standalone executable that doesn't require Python or terminal access.

## Quick Start

### Windows

1. **Run the build script:**
   ```cmd
   build_windows.bat
   ```

2. **Find your executable:**
   - Location: `dist/Tetris_Launcher.exe`
   - Double-click to run!

3. **Share with friends:**
   - Just send them the `Tetris_Launcher.exe` file
   - No Python needed, no terminal needed!

### macOS

1. **Run the build script:**
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

2. **Find your executable:**
   - Location: `dist/Tetris_Launcher.app`
   - Double-click to run!

3. **Share with friends:**
   - Send them the `Tetris_Launcher.app` file
   - They might need to right-click → Open the first time (security)

### Linux

1. **Run the build script:**
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

2. **Find your executable:**
   - Location: `dist/Tetris_Launcher`
   - Run with: `./dist/Tetris_Launcher`

3. **Share with friends:**
   - Send them the `Tetris_Launcher` file
   - They might need to: `chmod +x Tetris_Launcher` first

## What Gets Created

The build process creates a **GUI Launcher** that lets users:

1. ✅ Choose game mode with buttons (no terminal!)
2. ✅ Single Player - just click and play
3. ✅ Host LAN Game - enter port number
4. ✅ Join LAN Game - enter host IP and port

## Manual Build (Alternative)

If the scripts don't work, build manually:

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build the Launcher

```bash
pyinstaller --onefile --windowed \
    --name Tetris_Launcher \
    --add-data "game_logic:game_logic" \
    --add-data "rendering:rendering" \
    --add-data "networking:networking" \
    --hidden-import pygame \
    launcher.py
```

**Note:** On Windows, use semicolon (`;`) instead of colon (`:`) in `--add-data` paths:
```cmd
--add-data "game_logic;game_logic"
```

### 3. Find Your Executable

Look in the `dist/` folder for:
- Windows: `Tetris_Launcher.exe`
- macOS: `Tetris_Launcher.app`
- Linux: `Tetris_Launcher`

## File Sizes

Expected executable sizes:
- Windows: ~15-25 MB
- macOS: ~20-30 MB
- Linux: ~15-25 MB

These include everything needed to run the game!

## Distribution

### For Your Friends on School/Work Computers

1. **Copy the executable** to a USB drive or cloud storage
2. **Share the file** (Discord, Google Drive, etc.)
3. **Run it** - just double-click, no installation needed!
4. **Firewall** - they might need to allow network access for multiplayer

### Network Play Setup

Once everyone has the executable:

1. **Host player:**
   - Run the launcher
   - Click "Host LAN Game"
   - Enter port (default: 5555)
   - Share their IP address with friends

2. **Joining players:**
   - Run the launcher
   - Click "Join LAN Game"
   - Enter host's IP and port
   - Click "Connect"

## Troubleshooting

### "Build failed" Error

**Solution:** Make sure you have all dependencies:
```bash
pip install -r requirements-dev.txt
```

### Executable Won't Run (Windows)

**Solution:** Windows Defender might block it
- Right-click → Properties → Check "Unblock"
- Or add to Windows Defender exceptions

### Executable Won't Open (macOS)

**Solution:** macOS Gatekeeper blocks unsigned apps
- Right-click → Open (instead of double-click)
- Click "Open" in the security dialog
- Or: System Preferences → Security & Privacy → "Open Anyway"

### "ModuleNotFoundError" When Running

**Solution:** Rebuild with all hidden imports:
```bash
pyinstaller --onefile --windowed \
    --hidden-import pygame \
    --hidden-import game_logic \
    --hidden-import rendering \
    --hidden-import networking \
    launcher.py
```

### Executable is Too Large

**Solution:** Use UPX compression (optional):
```bash
pip install upx
pyinstaller --onefile --windowed --upx-dir /path/to/upx launcher.py
```

## Advanced Options

### Custom Icon

Add your own icon:
```bash
pyinstaller --onefile --windowed --icon=tetris.ico launcher.py
```

Icon requirements:
- Windows: `.ico` file
- macOS: `.icns` file
- Linux: `.png` file

### Reduce Size

Remove unnecessary files:
```bash
pyinstaller --onefile --windowed \
    --exclude-module tkinter.test \
    --exclude-module pydoc \
    launcher.py
```

### Debug Mode

If executable crashes, build with console for debugging:
```bash
pyinstaller --onefile \  # Remove --windowed
    --debug all \
    launcher.py
```

## Building for Other Platforms

**Important:** PyInstaller creates executables for the platform you build on:
- Build on Windows → Windows .exe
- Build on macOS → macOS .app
- Build on Linux → Linux binary

You **cannot** build a Windows .exe on macOS (cross-compilation not supported).

## Clean Build

To start fresh:

**Windows:**
```cmd
rmdir /s /q build dist
del *.spec
```

**macOS/Linux:**
```bash
rm -rf build dist *.spec
```

Then rebuild using the build scripts.

## Security Note

Some antivirus software may flag PyInstaller executables as suspicious (false positive). This is normal for packed executables. Your friends can:
- Add to antivirus exceptions
- Scan with VirusTotal to verify it's safe
- Use the --debug option to build with debug symbols

## Need Help?

If you encounter issues:
1. Check the [PyInstaller documentation](https://pyinstaller.org/)
2. Make sure all dependencies are installed
3. Try a clean build
4. Check the console output for specific errors

