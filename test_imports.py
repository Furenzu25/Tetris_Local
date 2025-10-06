#!/usr/bin/env python3
"""
Simple test launcher to debug the issue.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing imports...")
    
    # Test basic imports
    import pygame
    print("✓ pygame imported")
    
    import tkinter as tk
    print("✓ tkinter imported")
    
    # Test game modules
    from game_logic import GameEngine
    print("✓ GameEngine imported")
    
    from rendering import Renderer
    print("✓ Renderer imported")
    
    from networking import GameClient
    print("✓ GameClient imported")
    
    print("\n✓ All imports successful!")
    print("The issue might be in the GUI launcher code.")
    
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()

