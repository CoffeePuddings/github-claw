#!/bin/bash
set -e

echo "🚀 Setting up Media Processing Platform development environment..."

# Install FFmpeg
echo "📦 Installing FFmpeg..."
sudo apt-get update && sudo apt-get install -y ffmpeg

# Install Python backend dependencies
echo "🐍 Installing Python backend dependencies..."
cd media-platform/backend
pip install -r requirements.txt

# Initialize the database
echo "🗄️ Initializing SQLite database..."
python -c "from database import init_db; init_db()"

# Install Node.js frontend dependencies
echo "📦 Installing Vue frontend dependencies..."
cd ../frontend
npm install

echo "✅ Development environment setup complete!"
echo ""
echo "To start the services manually:"
echo "  Backend:  cd media-platform/backend && python app.py"
echo "  Frontend: cd media-platform/frontend && npm run dev"
