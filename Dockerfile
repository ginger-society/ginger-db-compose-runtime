FROM debian:bullseye-slim

# Update and install dependencies
RUN apt update && apt install -y \
    postgresql-client \
    libssl-dev \
    libpq-dev \
    pkg-config \
    curl \
    nano \
    make \
    gcc \
    wget \
    build-essential \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncurses5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    zlib1g-dev \
    tk-dev \
    libgdbm-dev \
    libnss3-dev \
    libdb5.3-dev \
    xz-utils \
    procps

# Download Python 3.11 source code
RUN wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz && \
    tar -xf Python-3.11.0.tgz

# Build and install Python 3.11
WORKDIR /Python-3.11.0
RUN ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall

# Ensure the new Python version is available
RUN python3.11 --version

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash - && \
    apt install -y nodejs

# Install Java
RUN apt install -y default-jdk

# Install OpenAPI Generator CLI globally
RUN npm install @openapitools/openapi-generator-cli -g

# Install CLI tools via your script
RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/ginger-society/infra-as-code-repo/main/rust-helpers/install-pipeline-clis.sh)"

ARG GINGER_TOKEN
ENV GINGER_TOKEN=$GINGER_TOKEN
RUN ginger-auth token-login $GINGER_TOKEN

# Set up app environment
ENV env prod
WORKDIR /app
COPY . /app

# Use ginger-connector
RUN ginger-connector refer stage && ginger-connector connect stage

EXPOSE 80

# Install Python requirements
RUN pip3.11 install -r requirements.txt

# Make script executable
RUN chmod +x run.sh

# Command to run the app
CMD ["/bin/bash", "run.sh"]
