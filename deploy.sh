echo "🚀 Starting Deployment..."

# Pull latest image
docker pull boppudimurali/lone-mlops:latest

# Stop & remove old container
docker stop lone-app 2>/dev/null || true
docker rm lone-app 2>/dev/null || true

# Run new container
docker run -d \
  --name lone-app \
  -p 8000:8000 \
  --restart always \
  boppudimurali/lone-mlops:latest

echo "✅ Deployment Complete! App running on port 8000"