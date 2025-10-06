#!/bin/bash
# Quick launcher for joining a LAN game

if [ -z "$1" ]; then
    echo "Usage: ./run_join.sh <host_ip> [port]"
    echo "Example: ./run_join.sh 192.168.1.100 5555"
    exit 1
fi

HOST=$1
PORT=${2:-5555}

echo "Joining Tetris game at $HOST:$PORT..."
python3 main.py --mode join --host $HOST --port $PORT

