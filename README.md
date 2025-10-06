# Tetris LAN Multiplayer

A modern Tetris game with LAN multiplayer support and TETR.IO-style preview system.

## Features

- Classic Tetris gameplay with modern controls
- TETR.IO format: Preview next 2 pieces
- LAN multiplayer support
- Real-time game synchronization
- Clean, organized codebase following SOLID principles

## Architecture

### Core Components

1. **Game Logic** (`game_logic/`)
   - Board management
   - Piece definitions and rotation
   - Collision detection
   - Line clearing
   - Scoring system

2. **Rendering** (`rendering/`)
   - Game board rendering
   - Piece preview rendering
   - UI elements

3. **Networking** (`networking/`)
   - LAN server
   - Client connection
   - Game state synchronization

4. **Main Application** (`main.py`)
   - Game initialization
   - Main game loop
   - Event handling

## Requirements

- Python 3.8+
- pygame
- Standard library (socket, threading, json)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Single Player
```bash
python main.py --mode single
```

### Host LAN Game
```bash
python main.py --mode host --port 5555
```

### Join LAN Game
```bash
python main.py --mode join --host 192.168.1.100 --port 5555
```

## Controls

- **Left/Right Arrow**: Move piece
- **Down Arrow**: Soft drop
- **Space**: Hard drop
- **Up Arrow / X**: Rotate clockwise
- **Z**: Rotate counter-clockwise
- **C**: Hold piece
- **ESC**: Pause/Menu

## Design Principles

- Single Responsibility: Each module handles one aspect
- Centralized Logic: All game rules in one place
- Environment Aware: Supports different game modes
- No Duplication: Shared logic is abstracted

