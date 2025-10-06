#!/usr/bin/env python3
"""
Tetris LAN Multiplayer - Main Entry Point

A modern Tetris game with LAN multiplayer support and TETR.IO-style preview.
"""

import argparse
import sys
from game_controller import GameController


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Tetris LAN Multiplayer Game',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Single player:
    python main.py --mode single
  
  Host a LAN game:
    python main.py --mode host --port 5555
  
  Join a LAN game:
    python main.py --mode join --host 192.168.1.100 --port 5555

Controls:
  Arrow Keys: Move left/right/down
  Up/X: Rotate clockwise
  Z: Rotate counter-clockwise
  Space: Hard drop
  C: Hold piece
  ESC: Pause
  R: Restart (when game over)
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['single', 'host', 'join'],
        default='single',
        help='Game mode (default: single)'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='Server host address for join mode (default: localhost)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5555,
        help='Port number for networking (default: 5555)'
    )
    
    parser.add_argument(
        '--name',
        type=str,
        default='Player',
        help='Player name (default: Player)'
    )
    
    return parser.parse_args()


def print_welcome():
    """Print welcome banner."""
    print("=" * 60)
    print("  TETRIS LAN MULTIPLAYER")
    print("  TETR.IO Format - Next 2 Pieces Preview")
    print("=" * 60)
    print()


def validate_args(args):
    """
    Validate command-line arguments.
    
    Args:
        args (argparse.Namespace): Parsed arguments
    
    Returns:
        bool: True if valid, False otherwise
    """
    if args.mode == 'join' and not args.host:
        print("Error: --host is required for join mode")
        return False
    
    if args.port < 1024 or args.port > 65535:
        print("Error: Port must be between 1024 and 65535")
        return False
    
    return True


def main():
    """Main entry point."""
    print_welcome()
    
    # Parse arguments
    args = parse_arguments()
    
    # Validate arguments
    if not validate_args(args):
        sys.exit(1)
    
    # Print mode information
    if args.mode == 'single':
        print("Starting single player game...")
    elif args.mode == 'host':
        print(f"Starting as host on port {args.port}...")
        print("Waiting for players to connect...")
    elif args.mode == 'join':
        print(f"Connecting to {args.host}:{args.port}...")
    
    print()
    
    # Create and run game controller
    try:
        controller = GameController(
            mode=args.mode,
            host=args.host if args.mode == 'join' else None,
            port=args.port
        )
        controller.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

