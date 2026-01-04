FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# dependensi OS minimal
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# copy project code (nanti folder app/)
COPY app /app

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
