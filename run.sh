#!/bin/bash

# Architecture Diagram Generator Startup Script

echo "🏗️  Architecture Diagram Generator"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/.requirements_installed" ]; then
    echo "📥 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.requirements_installed
else
    echo "✅ Dependencies already installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your Google API key"
    echo ""
fi

# Check if Graphviz is installed
if ! command -v dot &> /dev/null; then
    echo "⚠️  Graphviz not found! Please install it:"
    echo "   Ubuntu/Debian: sudo apt-get install graphviz"
    echo "   macOS: brew install graphviz"
    echo "   Windows: Download from https://graphviz.org/download/"
    echo ""
fi

# Create outputs directory
mkdir -p outputs

echo ""
echo "🚀 Starting Streamlit app..."
echo ""

streamlit run app.py
