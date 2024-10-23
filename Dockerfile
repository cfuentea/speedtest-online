FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    xvfb \
    chromium \
    && rm -rf /var/lib/apt/lists/*

COPY ./chromedriver-linux64 /app/chromedriver-linux64

RUN chmod +x /app/chromedriver-linux64/chromedriver

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install selenium

COPY . .

ENV DISPLAY=:99
CMD ["python", "./test_selenium.py"]

