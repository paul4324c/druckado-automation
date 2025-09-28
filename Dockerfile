FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY druckado_automation.py .
COPY config.ini .

RUN mkdir -p /app/orders

ENV LIVE_MODE=false

CMD ["python", "druckado_automation.py"]
