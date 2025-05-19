FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

RUN apt-get update && apt-get install -y \
    xvfb libglib2.0-0 libgtk-3-0 libdrm2 libnss3 libxss1 libasound2 libxshmfence1 \
    --no-install-recommends && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps

CMD ["python", "main.py"]