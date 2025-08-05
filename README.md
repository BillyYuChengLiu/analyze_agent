# Problem Resolve Service

一個基於Python和Google ADK的智能問題分析與解決服務，專門用於接收Graylog日誌、分析問題原因並提出解決方案。

## 功能特性

- 🔍 **智能日誌分析**: 接收並分析Graylog日誌
- 🤖 **問題診斷**: 自動識別問題原因
- 💡 **解決方案生成**: 提供具體的解決建議
- 🔄 **A2A協議**: 支援Agent-to-Agent通信
- ☁️ **Google Cloud整合**: 使用MCP協議在Google Cloud上運行
- 📊 **監控與指標**: 提供服務健康狀態監控

## 架構組件

```
problem-resolve-service/
├── src/
│   ├── core/           # 核心服務邏輯
│   ├── graylog/        # Graylog日誌處理
│   ├── analysis/       # 問題分析引擎
│   ├── mcp/           # MCP協議實現
│   ├── a2a/           # A2A協議實現
│   └── api/           # REST API接口
├── config/            # 配置文件
├── tests/             # 測試文件
└── deployment/        # 部署配置
```

## 技術要求

- **Python 3.13** - 穩定版本 (推薦使用最新穩定版)
- **Docker** - 容器化部署
- **Redis** - 緩存和隊列
- **Graylog** - 日誌收集
- **Google Cloud** - 雲端服務

### Python版本檢查
```bash
python --version
# 應該顯示: Python 3.13.x
```

## 快速開始

### 1. 安裝依賴
```bash
# 確保使用Python 3.13
python --version  # 應該顯示 Python 3.13.x

# 使用pip安裝依賴
pip install -r requirements.txt

# 或者使用現代化的安裝方式
pip install -e .
```

### 2. 配置環境變數
```bash
cp .env.example .env
# 編輯 .env 文件，填入您的Google Cloud憑證和Graylog配置
```

### 3. 啟動服務
```bash
python -m src.main
```

## 配置說明

### Google Cloud配置
- `GOOGLE_APPLICATION_CREDENTIALS`: Google Cloud服務帳戶金鑰
- `PROJECT_ID`: Google Cloud項目ID
- `REGION`: 部署區域

### Graylog配置
- `GRAYLOG_HOST`: Graylog服務器地址
- `GRAYLOG_PORT`: Graylog端口
- `GRAYLOG_USERNAME`: 用戶名
- `GRAYLOG_PASSWORD`: 密碼

### MCP配置
- `MCP_ENDPOINT`: MCP服務端點
- `MCP_API_KEY`: MCP API金鑰

## API文檔

服務啟動後，可訪問 `http://localhost:8000/docs` 查看完整的API文檔。

## 部署

### Google Cloud Run
```bash
gcloud run deploy problem-resolve-service \
  --source . \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated
```

### Docker
```bash
# 構建Python 3.13版本的鏡像
docker build -t problem-resolve-service .
docker run -p 8000:8000 problem-resolve-service
```

## 監控

服務提供以下監控端點：
- `/health`: 健康檢查
- `/metrics`: Prometheus指標
- `/logs`: 日誌查看

## 貢獻

歡迎提交Issue和Pull Request來改善這個服務。 