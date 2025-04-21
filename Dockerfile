FROM python:3.11-slim-bullseye

RUN apt update
RUN apt install postgresql-client libssl-dev libpq-dev pkg-config curl -y
RUN apt install -y curl nano make gcc wget build-essential procps

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash -
RUN apt install -y nodejs

# Install Java
RUN apt install -y default-jdk

# Install OpenAPI Generator CLI globally
RUN npm install @openapitools/openapi-generator-cli -g

# Install Ginger Society CLI tools
RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/ginger-society/infra-as-code-repo/main/rust-helpers/install-pipeline-clis.sh)"

ARG GINGER_TOKEN
ENV GINGER_TOKEN=$GINGER_TOKEN

# Set default environment to `stage`, but allow override
ARG GINGER_ENV=stage
ENV GINGER_ENV=$GINGER_ENV

RUN ginger-auth token-login $GINGER_TOKEN

# this env is for the ginger-dj env , it enables DEBUG=True/False
ENV env prod 
WORKDIR /app
COPY . /app

# Switch environment based on build argument
RUN if [ "$GINGER_ENV" = "prod" ]; then \
      ginger-connector refer prod && \
      ginger-connector connect prod; \
    else \
      ginger-connector refer stage && \
      ginger-connector connect stage; \
    fi

EXPOSE 80
RUN pip install -r requirements.txt
RUN chmod +x run.sh
RUN chmod +x migrate.sh
RUN chmod +x dry-run-makemigrate.sh

