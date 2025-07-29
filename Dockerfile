FROM python:3.13--bookworm

RUN apt-get update && \
    apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install playwright==@1.53.0 && \
    playwright install --with-deps

WORKDIR /app

RUN mkdir -p /assets/applicants/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD alembic upgrade head && python main.py
