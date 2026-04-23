

export GINGER_TOKEN=$(jq -r '.API_TOKEN' "$HOME/.ginger-society/auth.json")

docker buildx build -t gingersociety/db-compose-runtime-prod:latest . \
  --build-arg GINGER_TOKEN="$GINGER_TOKEN" \
  --build-arg GINGER_ENV=prod


