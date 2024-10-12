#!/bin/bash

pip install -r requirements.txt

docker run -d -p 6379:6379 --name redis redis

echo "Starting FastAPI server with uvicorn..."
uvicorn main:app --reload

# Instructions to access Swagger UI
echo "---------------------------------------------------"
echo "FastAPI is now running!"
echo "Access Swagger UI at: http://localhost:8000/docs"
echo "Redis is running on port 6379"
echo "---------------------------------------------------"
