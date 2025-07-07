FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY dns_sync.py ./
CMD ["python", "dns_sync.py"]
