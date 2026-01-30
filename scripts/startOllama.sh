#!/bin/bash
# Simple script to start Ollama if it's not already running

set -e

echo "Checking Ollama status..."

# Check if Ollama is already running
if pgrep -x ollama >/dev/null 2>&1; then
    echo "✓ Ollama is already running"
    ollama list 2>/dev/null || echo "Models not yet loaded"
    exit 0
fi

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Start Ollama
echo "Starting Ollama..."
nohup ollama serve > /workspaces/ae-security/ollama.log 2>&1 < /dev/null &

# Wait a moment for startup
sleep 3

# Check if it started successfully
if pgrep -x ollama >/dev/null 2>&1; then
    echo "✓ Ollama started successfully"
    echo "Available models:"
    ollama list 2>/dev/null || echo "No models loaded yet"
else
    echo "✗ Failed to start Ollama"
    echo "Check logs: cat /workspaces/ae-security/ollama.log"
    exit 1
fi

