# Use a lightweight official Python image
FROM python:3.12-slim

# Prevents Python from writing .pyc files and buffers logs directly to stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (remove unnecessary ones for your case)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker caching
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend source code
COPY . /app

# Expose internal port used by Uvicorn
EXPOSE 8000

# Default command to run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
