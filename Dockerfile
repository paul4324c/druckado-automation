# Base image
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget unzip libgl1 && \
    apt-get clean

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy script and config
COPY druckado_automation.py /app/druckado_automation.py
COPY config.ini /app/config.ini

# Create orders directory
RUN mkdir -p /app/orders

# Set working directory
WORKDIR /app

# Run the worker continuously
CMD ["python3", "druckado_automation.py"]
