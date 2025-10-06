#!/usr/bin/env python3
"""
Simple Tetris launcher - goes straight to single player mode.
No GUI needed, just runs the game directly.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        print("Starting Tetris...")
        
        # Import and run single player game
        from game_controller import GameController
        
        print("✓ Game controller loaded")
        print("Starting single player mode...")
        print("Press ESC to pause, R to restart when game over")
        
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

