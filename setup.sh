#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Step 1: Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Step 3: Install required dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Step 4: Start Redis using Docker
echo "Starting Redis using Docker..."
docker run -d -p 6379:6379 --name redis redis

# Step 5: Set up yfinance caching
echo "Setting up requests_cache for yfinance..."
# yfinance caching is handled by requests_cache which is set in the Python code

# Step 6: Start the FastAPI server using uvicorn
echo "Starting FastAPI server with uvicorn..."
uvicorn main:app --reload

# Instructions to access Swagger UI
echo "---------------------------------------------------"
echo "FastAPI is now running!"
echo "Access Swagger UI at: http://localhost:8000/docs"
echo "Redis is running on port 6379"
echo "---------------------------------------------------"
