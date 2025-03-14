FROM python:3.10-slim

WORKDIR /app

# Install dependencies for running Chromium
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libexpat1 \
    libatspi2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libasound2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the proxy code into the container
COPY proxy.py /app/

# Install Python dependencies and Playwright.
RUN pip install Flask playwright && playwright install

EXPOSE 8080

CMD ["python", "proxy.py"]
