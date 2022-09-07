# Base image
FROM python:3.10-slim

# Configure environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        gcc \
        libpq-dev \
        musl-dev \
        libc-dev \
        libcurl4-gnutls-dev \
        librtmp-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY ./requirements/requirements.txt /app/requirements.txt
COPY ./requirements/requirements.lint.txt /app/requirements.lint.txt
COPY ./requirements/requirements.test.txt /app/requirements.test.txt
COPY ./requirements/requirements.dev.txt /app/requirements.dev.txt

# Install project dependencies
RUN pip install --upgrade pip-tools
RUN pip-sync requirements.txt requirements.*.txt

# Expose port
EXPOSE 8005

# Copy configuration files
COPY ./conf /app/conf
RUN chmod +x /app/conf/docker/entrypoint.sh

# Copy project files
COPY . .

# Spin up server
WORKDIR /app/src
CMD ["/app/conf/docker/entrypoint.sh"]
