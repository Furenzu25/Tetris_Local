# Quick Start Guide

## Installation

1. **Install Python 3.8 or higher** (if not already installed)
   ```bash
   python3 --version
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or with pip3:
   ```bash
   pip3 install -r requirements.txt
   ```

## Running the Game

### Single Player Mode

Play Tetris offline:
```bash
python main.py --mode single
```

### LAN Multiplayer Mode

#### Option 1: Host a Game

One player hosts the game server:
```bash
python main.py --mode host --port 5555
```

The host will see their IP address. Share this with other players.

To find your IP address:
- **macOS/Linux**: `ifconfig | grep "inet " | grep -v 127.0.0.1`
- **Windows**: `ipconfig`

#### Option 2: Join a Game

Other players join using the host's IP:
```bash
python main.py --mode join --host 192.168.1.100 --port 5555
```

Replace `192.168.1.100` with the actual host IP address.

## Testing Locally

You can test multiplayer on the same computer:

**Terminal 1** (Host):
```bash
python main.py --mode host --port 5555
```

**Terminal 2** (Join):
```bash
python main.py --mode join --host localhost --port 5555
```

## Network Requirements

- All players must be on the **same local network** (LAN)
- Firewall may need to allow connections on the chosen port
- Default port is 5555 (can be changed with `--port`)

## Troubleshooting

### "Connection refused"
- Make sure the host started the server first
- Check that you're using the correct IP address
- Verify the port number matches on both host and client
- Check firewall settings

### "Port already in use"
- Choose a different port number with `--port` option
- Make sure no other instance is running

### Game runs slowly
- Close other applications
- Check system resources
- Try reducing preview windows if modified

## Game Features

✅ Classic Tetris gameplay  
✅ TETR.IO format with next 2 pieces preview  
✅ Ghost piece showing landing position  
✅ Hold piece functionality  
✅ LAN multiplayer with opponent board view  
✅ Real-time game synchronization  
✅ Scoring system with combos  
✅ Progressive difficulty (levels)  

## Controls

See [CONTROLS.md](CONTROLS.md) for complete control reference.

## Need Help?

- Check [README.md](README.md) for detailed documentation
- Review [DESIGN.md](DESIGN.md) for architecture details
- See [CONTROLS.md](CONTROLS.md) for game controls

