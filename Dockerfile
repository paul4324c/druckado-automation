FROM ubuntu:22.04

# Install Python 3.10 and dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip wget unzip libgl1 && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    apt-get clean

WORKDIR /app

# Copy your files
COPY requirements.txt /app/requirements.txt
COPY druckado_automation.py /app/druckado_automation.py
COPY config.ini /app/config.ini

# Install Python packages
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

# Create orders directory
RUN mkdir -p /app/orders

# Start the automation script
CMD ["python3", "/app/druckado_automation.py"]
