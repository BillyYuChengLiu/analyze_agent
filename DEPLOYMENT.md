# 部署指南

## 專案概述

這是一個基於 Google ADK 的智能問題分析與建議服務，使用 Gemini 2.0 Flash 模型來分析計畫書和 Graylog 日誌，並提供問題診斷和解決建議。

## 系統需求

- **Python 3.13**
- **Docker** (用於容器化部署)
- **Google Cloud Platform** 帳戶
- **Git**

## 本地測試

### 1. 克隆專案

```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. 使用 Docker Compose 啟動

```bash
# 啟動服務
docker-compose -f docker-compose.analyze-problem.yml up --build

# 或背景執行
docker-compose -f docker-compose.analyze-problem.yml up --build -d
```

### 3. 驗證服務

```bash
# 檢查服務狀態
curl http://localhost:8001/health

# 查看日誌
docker-compose -f docker-compose.analyze-problem.yml logs -f
```

### 4. 停止服務

```bash
docker-compose -f docker-compose.analyze-problem.yml down
```

## GCP 部署

### 方法一：Cloud Run (推薦)

#### 1. 準備環境

```bash
# 安裝 Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

# 登入 Google Cloud
gcloud auth login

# 設定專案
gcloud config set project YOUR_PROJECT_ID

# 啟用必要的 API
gcloud services enable run.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

#### 2. 部署到 Cloud Run

```bash
# 部署服務
gcloud run deploy analyze-problem \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8001 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=true \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10
```

#### 3. 驗證部署

```bash
# 獲取服務 URL
gcloud run services describe analyze-problem --region us-central1 --format="value(status.url)"

# 測試服務
curl https://your-service-url/health
```

### 方法二：Google Kubernetes Engine (GKE)

#### 1. 建立 Container Registry

```bash
# 設定 Docker 認證
gcloud auth configure-docker

# 建立 image
docker build -f Dockerfile.analyze-problem -t gcr.io/YOUR_PROJECT_ID/analyze-problem:latest .

# 推送到 Container Registry
docker push gcr.io/YOUR_PROJECT_ID/analyze-problem:latest
```

#### 2. 建立 GKE 叢集

```bash
# 建立叢集
gcloud container clusters create analyze-problem-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type e2-standard-2

# 獲取認證
gcloud container clusters get-credentials analyze-problem-cluster --zone us-central1-a
```

#### 3. 部署到 GKE

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: analyze-problem
spec:
  replicas: 3
  selector:
    matchLabels:
      app: analyze-problem
  template:
    metadata:
      labels:
        app: analyze-problem
    spec:
      containers:
      - name: analyze-problem
        image: gcr.io/YOUR_PROJECT_ID/analyze-problem:latest
        ports:
        - containerPort: 8001
        env:
        - name: GOOGLE_CLOUD_PROJECT
          value: "YOUR_PROJECT_ID"
        - name: GOOGLE_CLOUD_LOCATION
          value: "us-central1"
        - name: GOOGLE_GENAI_USE_VERTEXAI
          value: "true"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: analyze-problem-service
spec:
  selector:
    app: analyze-problem
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8001
  type: LoadBalancer
```

```bash
# 部署到 GKE
kubectl apply -f k8s-deployment.yaml

# 檢查部署狀態
kubectl get pods
kubectl get services
```

### 方法三：Compute Engine

#### 1. 建立 VM 實例

```bash
# 建立 VM
gcloud compute instances create analyze-problem-vm \
  --zone us-central1-a \
  --machine-type e2-standard-2 \
  --image-family ubuntu-2004-lts \
  --image-project ubuntu-os-cloud \
  --tags http-server,https-server

# 設定防火牆規則
gcloud compute firewall-rules create allow-analyze-problem \
  --allow tcp:8001 \
  --target-tags http-server \
  --source-ranges 0.0.0.0/0
```

#### 2. 在 VM 上部署

```bash
# SSH 到 VM
gcloud compute ssh analyze-problem-vm --zone us-central1-a

# 在 VM 內執行
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# 克隆專案並部署
git clone <your-repo-url>
cd <project-directory>
sudo docker build -f Dockerfile.analyze-problem -t analyze-problem .
sudo docker run -d --name analyze-problem-service -p 8001:8001 analyze-problem
```

## 環境變數說明

| 變數名稱 | 說明 | 預設值 | 必填 |
|---------|------|--------|------|
| `GOOGLE_CLOUD_PROJECT` | GCP 專案 ID | - | ✅ |
| `GOOGLE_CLOUD_LOCATION` | 部署區域 | us-central1 | ❌ |
| `GOOGLE_GENAI_USE_VERTEXAI` | 使用 Vertex AI | true | ❌ |

## 服務端點

### 健康檢查
```
GET /health
```

### A2A 端點
```
POST /a2a/v1/agents/{agent_id}/invoke
```

### 文檔
```
GET /docs
```

## 監控與日誌

### Cloud Run 日誌
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=analyze-problem" --limit 50
```

### GKE 日誌
```bash
kubectl logs -l app=analyze-problem
```

## 故障排除

### 常見問題

1. **認證錯誤**
   - 確保服務帳號有適當權限
   - 檢查 `GOOGLE_CLOUD_PROJECT` 設定

2. **記憶體不足**
   - 增加 Cloud Run 記憶體配置
   - 調整 GKE Pod 資源限制

3. **連接超時**
   - 檢查防火牆規則
   - 確認服務正在運行

### 除錯指令

```bash
# 檢查容器狀態
docker ps
docker logs <container-id>

# 檢查 GKE Pod 狀態
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# 檢查 Cloud Run 服務
gcloud run services describe analyze-problem --region us-central1
```

## 成本優化

### Cloud Run
- 使用最小實例數 0
- 設定適當的記憶體和 CPU 配置
- 監控請求量並調整配置

### GKE
- 使用 Spot 實例降低成本
- 設定適當的資源限制
- 使用 Horizontal Pod Autoscaler

## 安全建議

1. **網路安全**
   - 使用 VPC 網路隔離
   - 設定適當的防火牆規則

2. **身份驗證**
   - 使用 IAM 進行身份驗證
   - 定期輪換服務帳號金鑰

3. **資料安全**
   - 加密傳輸中的資料
   - 使用 Secret Manager 管理敏感資訊

## 更新部署

### Cloud Run
```bash
gcloud run deploy analyze-problem --source . --region us-central1
```

### GKE
```bash
kubectl set image deployment/analyze-problem analyze-problem=gcr.io/YOUR_PROJECT_ID/analyze-problem:latest
```

## 支援

如有問題，請檢查：
1. [Google Cloud 文檔](https://cloud.google.com/docs)
2. [Google ADK 文檔](https://ai.google.dev/docs)
3. 專案 Issues 頁面 