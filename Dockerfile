FROM debian:bookworm-slim
RUN apt update
RUN apt install postgresql-client python3.11 python3-pip libssl-dev libpq-dev pkg-config curl -y
RUN apt install -y curl nano make gcc wget build-essential procps

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



ENV env prod
WORKDIR /app
COPY . /app

RUN ginger-connector refer stage
RUN ginger-connector connect stage

EXPOSE 80
RUN pip install -r requirements.txt
RUN chmod +x run.sh
CMD ["/bin/bash", "run.sh"]
