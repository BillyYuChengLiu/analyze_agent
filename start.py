#!/usr/bin/env python3
"""
Problem Resolve Service 啟動腳本
"""

import os
import sys
import argparse
import asyncio
from pathlib import Path

# 添加項目根目錄到Python路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.main import main


def parse_args():
    """解析命令行參數"""
    parser = argparse.ArgumentParser(description="Problem Resolve Service")
    parser.add_argument(
        "--config",
        type=str,
        default=".env",
        help="配置文件路徑 (默認: .env)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="服務器主機 (默認: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="服務器端口 (默認: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="啟用自動重載"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="工作進程數量 (默認: 1)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="日誌級別 (默認: INFO)"
    )
    
    return parser.parse_args()


def setup_environment(args):
    """設置環境變數"""
    # 設置配置文件路徑
    if os.path.exists(args.config):
        os.environ["ENV_FILE"] = args.config
    
    # 設置服務器配置
    os.environ["SERVER_HOST"] = args.host
    os.environ["SERVER_PORT"] = str(args.port)
    os.environ["SERVER_RELOAD"] = str(args.reload).lower()
    os.environ["SERVER_WORKERS"] = str(args.workers)
    os.environ["LOG_LEVEL"] = args.log_level


def check_dependencies():
    """檢查依賴"""
    # 檢查Python版本
    import sys
    if sys.version_info < (3, 13):
        print(f"✗ Python版本過低: {sys.version}")
        print("請使用Python 3.13或更高版本")
        sys.exit(1)
    else:
        print(f"✓ Python版本: {sys.version}")
    
    try:
        import fastapi
        import uvicorn
        import pydantic
        import aiohttp
        import structlog
        print("✓ 所有依賴已安裝")
    except ImportError as e:
        print(f"✗ 缺少依賴: {e}")
        print("請運行: pip install -r requirements.txt")
        sys.exit(1)


def check_config():
    """檢查配置"""
    required_env_vars = [
        "GOOGLE_CLOUD_PROJECT_ID",
        "MCP_ENDPOINT",
        "MCP_API_KEY",
        "A2A_AGENT_ID",
        "A2A_ENDPOINT",
        "A2A_SECRET_KEY"
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"✗ 缺少必要的環境變數: {', '.join(missing_vars)}")
        print("請檢查 .env 文件或環境變數設置")
        return False
    
    print("✓ 配置檢查通過")
    return True


def main_wrapper():
    """主函數包裝器"""
    args = parse_args()
    
    print("🚀 啟動 Problem Resolve Service...")
    print(f"📁 項目根目錄: {project_root}")
    print(f"⚙️  配置文件: {args.config}")
    print(f"🌐 服務地址: {args.host}:{args.port}")
    print(f"🔄 自動重載: {args.reload}")
    print(f"👥 工作進程: {args.workers}")
    print(f"📝 日誌級別: {args.log_level}")
    print()
    
    # 檢查依賴
    check_dependencies()
    
    # 設置環境
    setup_environment(args)
    
    # 檢查配置
    if not check_config():
        sys.exit(1)
    
    print("✅ 所有檢查通過，正在啟動服務...")
    print()
    
    # 啟動服務
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 服務已停止")
    except Exception as e:
        print(f"❌ 服務啟動失敗: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main_wrapper() 