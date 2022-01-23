FROM python:3.8
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt \
    && useradd -U app_user

WORKDIR /app
USER app_user:app_user
COPY --chown=app_user:app_user . .
RUN chmod +x docker/*.sh

ENTRYPOINT [ "docker/entrypoint.sh" ]