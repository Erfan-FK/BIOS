FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1

# Copy application and requirements
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
WORKDIR /app
EXPOSE 8000
# Port for Daphne
EXPOSE 8001 

# Build arguments
ARG DEV=false
ARG DJANGO_ENV=development
ENV DJANGO_ENV=$DJANGO_ENV
ENV PATH="/py/bin:$PATH"

# Install 
RUN apk update && apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        postgresql-dev \
        libc-dev \
        linux-headers && \
    apk add --no-cache postgresql-client && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt && /py/bin/pip install watchdog; fi && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/* /tmp

# Create a non-root django-user
RUN adduser --disabled-password --no-create-home django-user

# Switch to non-root user
USER django-user
