FROM public.ecr.aws/docker/library/python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
COPY frontend/ ./frontend/
COPY config_management/ ./config_management/
ENV PYTHONPATH=/app
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8003
CMD ["python", "-m", "app.server"]