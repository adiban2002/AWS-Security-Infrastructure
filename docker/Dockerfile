FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 🚀 এটাকে /app এর বদলে শুধু রুট রাখো অথবা PYTHONPATH সেট করো
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 🚀 এই কপি করার স্টাইলটা খুব ইম্পর্ট্যান্ট
COPY config_management/ ./config_management/
COPY app/ ./app/

# 🚀 পাইথনকে বলে দাও রুটেই মডিউলগুলো খুঁজবে
ENV PYTHONPATH=/app

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8003
CMD ["python", "-m", "app.server"]