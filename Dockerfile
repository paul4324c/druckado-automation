FROM ubuntu:22.04

# Install Python 3 and dependencies
RUN apt-get update && \
    apt-get install -y python3.13 python3.13-venv python3-pip wget unzip libgl1 && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    apt-get clean

WORKDIR /app

# Copy all files
COPY requirements.txt /app/requirements.txt
COPY druckado_automation.py /app/druckado_automation.py
COPY config.ini /app/config.ini

# Install Python packages
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

# Create orders folder
RUN mkdir -p /app/orders

# Start the worker
CMD ["python3", "/app/druckado_automation.py"]
