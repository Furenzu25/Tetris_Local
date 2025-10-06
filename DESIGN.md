# Tetris LAN Game - Design Document

## Overview
A Tetris game with LAN multiplayer capabilities and TETR.IO-style piece preview system.

## Game Mechanics

### Core Tetris Rules
- 10x20 visible playfield (standard)
- 7 tetromino pieces (I, O, T, S, Z, J, L)
- SRS (Super Rotation System) for piece rotation
- Lock delay: 0.5 seconds
- Line clearing with scoring

### TETR.IO Features
- Show next 2 pieces in queue
- Piece preview panel on the right side
- Hold piece functionality
- Ghost piece (shows where piece will land)

### Scoring System
- Single: 100 points
- Double: 300 points
- Triple: 500 points
- Tetris (4 lines): 800 points
- Combo multiplier for consecutive clears

## Technical Architecture

### 1. Game Logic Layer (`game_logic/`)

#### `pieces.py`
- Tetromino definitions (shapes, colors)
- Rotation states for each piece
- Piece color constants

#### `board.py`
- Board state management (10x20 grid)
- Place piece on board
- Check collision
- Line clearing logic
- Board validation

#### `game_engine.py`
- Centralized game rules and logic
- Current piece management
- Piece queue (next 2 pieces visible)
- Hold piece functionality
- Score calculation
- Game state (running, paused, game over)
- Drop timing and gravity
- Lock delay handling

### 2. Rendering Layer (`rendering/`)

#### `renderer.py`
- Draw game board
- Draw current piece
- Draw ghost piece
- Draw piece preview (next 2)
- Draw hold piece
- Draw score and stats
- Draw grid lines

#### `colors.py`
- Color palette definitions
- Theme management

### 3. Networking Layer (`networking/`)

#### `server.py`
- LAN server implementation
- Client connection management
- Game state broadcasting
- Input synchronization
- Player management

#### `client.py`
- Connect to LAN server
- Send player inputs
- Receive game state updates
- Handle disconnection

#### `protocol.py`
- Network message definitions
- Serialization/deserialization
- Message types (CONNECT, INPUT, STATE_UPDATE, DISCONNECT)

### 4. Main Application

#### `main.py`
- Application entry point
- Command-line argument parsing
- Game mode selection
- Main game loop coordination

#### `game_controller.py`
- Handle user input
- Update game state
- Coordinate rendering
- Manage game modes (single/multi)

## Data Structures

### Board State
```python
{
    "grid": [[0 for x in range(10)] for y in range(20)],  # 0 = empty, >0 = color
    "current_piece": Piece,
    "piece_x": int,
    "piece_y": int,
    "next_pieces": [Piece, Piece],  # Next 2 pieces
    "hold_piece": Piece | None,
    "can_hold": bool,
    "score": int,
    "lines_cleared": int,
    "level": int,
    "game_over": bool
}
```

### Piece Structure
```python
{
    "type": str,  # 'I', 'O', 'T', 'S', 'Z', 'J', 'L'
    "rotation": int,  # 0-3
    "shape": [[bool]],  # 4x4 matrix
    "color": tuple  # RGB
}
```

### Network Message
```python
{
    "type": str,  # MESSAGE_TYPE
    "timestamp": float,
    "player_id": str,
    "data": dict
}
```

## Networking Protocol

### Connection Flow
1. Client connects to server via TCP socket
2. Server assigns player ID
3. Server sends initial game state
4. Game loop begins

### Message Types
- **CONNECT**: Initial connection request
- **CONNECTED**: Connection acknowledgment
- **INPUT**: Player input (move, rotate, drop)
- **STATE_UPDATE**: Full game state broadcast
- **LINE_CLEAR**: Line clear event
- **GAME_OVER**: Player game over
- **DISCONNECT**: Player disconnection

### Synchronization Strategy
- Server authoritative model
- Client sends inputs only
- Server processes inputs and broadcasts state
- 60 FPS update rate
- Delta compression for efficiency

## UI Layout

```
┌─────────────────────────────────────────────────┐
│  HOLD           TETRIS LAN        NEXT          │
│  ┌───┐                           ┌───┐          │
│  │   │                           │   │          │
│  └───┘                           └───┘          │
│                                  ┌───┐          │
│  ┌──────────────────────┐       │   │          │
│  │                      │       └───┘          │
│  │                      │                      │
│  │    GAME BOARD        │   SCORE: 0000        │
│  │      10 x 20         │   LINES: 0           │
│  │                      │   LEVEL: 1           │
│  │                      │                      │
│  │                      │   OPPONENT:          │
│  │                      │   ┌──────────┐       │
│  │                      │   │ Mini     │       │
│  │                      │   │ Board    │       │
│  └──────────────────────┘   └──────────┘       │
└─────────────────────────────────────────────────┘
```

## File Size Management
- Each file kept under 300 lines
- Logic split into focused modules
- Shared utilities extracted to separate files

## Development Phases

### Phase 1: Core Game (Single Player)
- Implement all game logic
- Basic rendering
- Input handling
- Preview system with 2 pieces

### Phase 2: Networking
- Server implementation
- Client implementation
- Protocol definition
- State synchronization

### Phase 3: Multiplayer Integration
- Connect networking to game logic
- Opponent board display
- Game start/end coordination

### Phase 4: Polish
- UI improvements
- Sound effects (optional)
- Settings menu
- Better error handling

