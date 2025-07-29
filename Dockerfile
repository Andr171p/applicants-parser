FROM python:3.13--bookworm

RUN apt-get update && \
    apt-get install -y \
    wget \
    xvfb \
    libgtk-3-0 \
    libnotify-dev \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install playwright==@1.53.0 && \
    playwright install --with-deps

WORKDIR /app

RUN mkdir -p /assets/applicants/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD xvfb-run --server-args="-screen 0 1280x1024x16" sh -c "alembic upgrade head && python main.py"

# CMD alembic upgrade head && python main.py
