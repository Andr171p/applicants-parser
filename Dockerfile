FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install playwright && \
    playwright install && \
    playwright install-deps

WORKDIR /app

RUN mkdir -p /assets/applicants/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD alembic upgrade head && python main.py
