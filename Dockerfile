# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Command to start FastAPI Server
CMD ["uvicorn", "app.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
