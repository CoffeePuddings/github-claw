#!/bin/bash
set -e

echo "🚀 Starting Media Processing Platform services..."

# Start Flask backend in background
echo "🐍 Starting Flask backend on port 5000..."
cd media-platform/backend
python app.py &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait a moment for backend to start
sleep 2

# Start Vue frontend dev server in background
echo "⚡ Starting Vue frontend on port 3000..."
cd ../frontend
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "✅ Services started!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:5000"
echo ""
echo "To stop services: kill $BACKEND_PID $FRONTEND_PID"
