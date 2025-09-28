# Use a stable Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY druckado_automation.py .
COPY config.ini .

# Create orders directory
RUN mkdir -p /app/orders

# Set environment variables if you want defaults (can override in Koyeb dashboard)
ENV LIVE_MODE=false

# Command to run your worker
CMD ["python", "druckado_automation.py"]
