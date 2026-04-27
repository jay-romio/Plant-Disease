# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create upload directory
RUN mkdir -p uploadimages

# Expose port (Cloud Run uses port 8080 by default)
EXPOSE 8080

# Set environment variables
ENV PORT=8080

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "mobile_app:app"]
