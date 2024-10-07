FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt update
RUN apt install postgresql-client libssl-dev libpq-dev pkg-config curl -y
RUN apt update && apt install -y curl nano make gcc wget build-essential procps


# Manually download and install libssl1.1 for compatibility
RUN apt-get install -y --no-install-recommends wget \
    && wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb \
    && dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb \
    && rm libssl1.1_1.1.0g-2ubuntu4_amd64.deb

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash -
RUN apt install -y nodejs

# Install Java
RUN apt install -y default-jdk

# Install OpenAPI Generator CLI globally
RUN npm install @openapitools/openapi-generator-cli -g

RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/ginger-society/infra-as-code-repo/main/rust-helpers/install-pipeline-clis.sh)"

ARG GINGER_TOKEN
ENV GINGER_TOKEN=$GINGER_TOKEN
RUN ginger-auth token-login $GINGER_TOKEN

RUN ginger-connector refer stage
RUN ginger-connector connect stage

ENV env prod
WORKDIR /app
COPY . /app
EXPOSE 80
RUN pip install -r requirements.txt
RUN chmod +x run.sh
CMD ["/bin/bash", "run.sh"]
