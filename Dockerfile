FROM python:3.10-slim

# Set working folder inside the container
WORKDIR /app

# Copy project files into container
COPY requirements.txt .
COPY druckado_automation.py .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Start script automatically
CMD ["python", "druckado_automation.py"]

