
# Example Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Ensure src is in PYTHONPATH if not installed as a package
ENV PYTHONPATH=/app/src:${PYTHONPATH}

CMD ["python", "src/main.py"]
