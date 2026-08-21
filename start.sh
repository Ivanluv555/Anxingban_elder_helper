#!/bin/bash
# 快速启动脚本

echo "🚀 启动安行伴后端服务..."
echo ""

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "❌ 虚拟环境不存在，请先执行："
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# 检查 .env 配置
if [ ! -f ".env" ]; then
    echo "❌ .env 文件不存在，请先配置数据库连接"
    exit 1
fi

# 启动服务
echo "📦 加载模块..."
export PYTHONPATH=$(pwd)

echo "🔗 连接数据库..."
.venv/bin/python -c "from app.database import engine, import_all_entities, Base; import_all_entities(); Base.metadata.create_all(bind=engine); print('✓ 数据库表已同步')"

echo ""
echo "🌐 启动 FastAPI 服务..."
echo "   API 文档: http://127.0.0.1:8000/docs"
echo "   前端页面: http://127.0.0.1:8000"
echo ""

.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
