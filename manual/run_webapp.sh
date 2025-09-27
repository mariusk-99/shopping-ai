#!/bin/bash

# Virtual Try-On Web Application Launcher
echo "🌟 Starting Virtual Try-On Web Application..."

# Check if we're in the right directory
if [ ! -f "webapp/app.py" ]; then
    echo "❌ Please run this script from the manual/ directory"
    echo "Current directory: $(pwd)"
    echo "Expected file: webapp/app.py"
    exit 1
fi

# Check Python dependencies
echo "🔧 Checking dependencies..."
python3 -c "import flask, dotenv, PIL" 2>/dev/null || {
    echo "❌ Missing dependencies. Installing..."
    python3 -m pip install Flask python-dotenv Pillow requests
}

# Check API key
if [ -f ".env" ]; then
    echo "✅ Found .env file"
else
    echo "⚠️  Warning: .env file not found"
    echo "Please ensure your Google Gemini API key is configured"
fi

# Start the Flask application
echo "🚀 Starting server..."
echo "📱 Access the application at: http://localhost:5000"
echo "🔗 Or try: http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd webapp
export FLASK_ENV=development
python3 app.py