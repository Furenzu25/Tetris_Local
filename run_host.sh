#!/bin/bash
# Quick launcher for hosting a LAN game

PORT=${1:-5555}

echo "Starting Tetris as HOST on port $PORT..."
echo ""
echo "Your IP addresses:"
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print "  - " $2}'
echo ""
echo "Share one of these IPs with other players"
echo ""

python3 main.py --mode host --port $PORT

