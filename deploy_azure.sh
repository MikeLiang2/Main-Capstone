#!/bin/bash
set -e

# ===== 基本变量 =====
RESOURCE_GROUP="capstone"
LOCATION="westus"
ACR_NAME="capstoneacr"
POSTGRES_SERVER="capstone-db"
POSTGRES_USER="pgadmin"
POSTGRES_PASSWORD="password"
POSTGRES_DB="checklist"
APP_NAME="capstoneapp"

# ===== 读取 GEMINI_API_KEY =====
if [ -z "$GEMINI_API_KEY" ] && [ -f ".env" ]; then
  GEMINI_API_KEY=$(grep -E '^GEMINI_API_KEY=' .env | head -n1 | cut -d'=' -f2-)
fi
if [ -z "$GEMINI_API_KEY" ]; then
  echo "⚠️  GEMINI_API_KEY 未设置（环境变量或 .env）。"
fi

# Load Azure environment variables if not set
for var in AZURE_OPENAI_ENDPOINT AZURE_OPENAI_API_KEY AZURE_OPENAI_DEPLOYMENT AZURE_STORAGE_ACCOUNT AZURE_STORAGE_KEY PERM_CONTAINER
do
  if [ -z "${!var}" ] && [ -f ".env" ]; then
    export $var=$(grep -E "^${var}=" .env | head -n1 | cut -d'=' -f2-)
  fi
  if [ -z "${!var}" ]; then
    echo "⚠️  $var is not set"
  fi
done

echo "🔹 Logging into Azure..."
az login

# ===== PostgreSQL 连接信息 =====
POSTGRES_HOST="$POSTGRES_SERVER.postgres.database.azure.com"
DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB}"

echo "🔹 Creating .env.prod..."
cat <<EOF > .env.prod
DATABASE_URL=${DATABASE_URL}
EOF

# ===== ACR 登录 & 获取凭据 =====
echo "🔹 Logging into ACR..."
az acr login --name $ACR_NAME
ACR_USER=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASS=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

# # # ===== 构建并推送后端镜像 =====
# echo "🔹 Building & pushing backend images..."
docker build -t $ACR_NAME.azurecr.io/backend:latest ./backend
docker push $ACR_NAME.azurecr.io/backend:latest

# # # ===== 创建 Container Apps 环境 =====
# echo "🔹 Creating Azure Container Apps Environment..."
# az containerapp env create \
#   --name ${APP_NAME}-env \
#   --resource-group $RESOURCE_GROUP \
#   --location $LOCATION \
#   --logs-destination none

# ===== 部署 backend =====
echo "🔹 Creating backend Container App..."
az containerapp create \
  --name ${APP_NAME}-backend \
  --resource-group $RESOURCE_GROUP \
  --environment ${APP_NAME}-env \
  --image $ACR_NAME.azurecr.io/backend:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server $ACR_NAME.azurecr.io \
  --registry-username "$ACR_USER" \
  --registry-password "$ACR_PASS" \
  --env-vars DATABASE_URL="${DATABASE_URL}" \
             POSTGRES_HOST="${POSTGRES_HOST}" \
             POSTGRES_PORT="5432" \
             GEMINI_API_KEY="${GEMINI_API_KEY}" \
             ALLOWED_ORIGINS="http://localhost:5173" \
             AZURE_OPENAI_ENDPOINT="${AZURE_OPENAI_ENDPOINT}" \
             AZURE_OPENAI_API_KEY="${AZURE_OPENAI_API_KEY}" \
             AZURE_OPENAI_DEPLOYMENT="${AZURE_OPENAI_DEPLOYMENT}" \
             AZURE_STORAGE_ACCOUNT="${AZURE_STORAGE_ACCOUNT}" \
             AZURE_STORAGE_KEY="${AZURE_STORAGE_KEY}" \
             PERM_CONTAINER="${PERM_CONTAINER}" \
             TEMP_CONTAINER="${TEMP_CONTAINER}"

# ===== 获取 backend URL =====
echo "🔹 Fetching backend URL..."
BACKEND_FQDN=$(az containerapp show \
  --name ${APP_NAME}-backend \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)
echo "Backend URL: https://${BACKEND_FQDN}"

# ===== 构建并推送前端镜像（注入真实 API 地址）=====
echo "🔹 Building & pushing frontend image..."
docker build \
  --build-arg VITE_API_BASE_URL="https://${BACKEND_FQDN}" \
  -t $ACR_NAME.azurecr.io/frontend:latest \
  -f ./frontend/Dockerfile.prod ./frontend
docker push $ACR_NAME.azurecr.io/frontend:latest

# ===== 部署 frontend =====
echo "🔹 Creating frontend Container App..."
az containerapp create \
  --name ${APP_NAME}-frontend \
  --resource-group $RESOURCE_GROUP \
  --environment ${APP_NAME}-env \
  --image $ACR_NAME.azurecr.io/frontend:latest \
  --target-port 80 \
  --ingress external \
  --registry-server $ACR_NAME.azurecr.io \
  --registry-username "$ACR_USER" \
  --registry-password "$ACR_PASS"

# ===== 获取 frontend URL，并回写到 backend 的 CORS 白名单 =====
echo "🔹 Fetching frontend URL..."
FRONTEND_FQDN=$(az containerapp show \
  --name ${APP_NAME}-frontend \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)
echo "Frontend URL: https://${FRONTEND_FQDN}"

echo "🔹 Updating backend CORS origins..."
az containerapp update \
  --name ${APP_NAME}-backend \
  --resource-group $RESOURCE_GROUP \
  --set-env-vars \
      DATABASE_URL="${DATABASE_URL}" \
      POSTGRES_HOST="${POSTGRES_HOST}" \
      POSTGRES_PORT="5432" \
      GEMINI_API_KEY="${GEMINI_API_KEY}" \
      ALLOWED_ORIGINS="https://${FRONTEND_FQDN},http://localhost:5173"

echo "✅ Deployment completed!"
echo "Frontend URL: https://${FRONTEND_FQDN}"
echo "Backend URL:  https://${BACKEND_FQDN}"