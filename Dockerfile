# Use Ubuntu as base
FROM ubuntu:22.04

# Install Python and necessary libraries
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget unzip libgl1 && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy files into container
COPY requirements.txt /app/requirements.txt
COPY druckado_automation.py /app/druckado_automation.py
COPY config.ini /app/config.ini

# Install Python dependencies
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Create orders folder
RUN mkdir -p /app/orders

# Start the script
CMD ["python3", "/app/druckado_automation.py"]
