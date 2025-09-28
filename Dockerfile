# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script and config
COPY druckado_automation.py .
COPY config.ini .

# Create orders folder
RUN mkdir -p /app/orders

# Set environment variable defaults (optional)
ENV LIVE_MODE=false

# Command to run the worker
CMD ["python", "druckado_automation.py"]
