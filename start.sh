#!/bin/bash

# CN2Global 快速启动脚本

echo "🚀 CN2Global 启动脚本"
echo "====================="

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    exit 1
fi

echo "✅ Node.js 版本: $(node -v)"

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装"
    exit 1
fi

echo "✅ npm 版本: $(npm -v)"

# 进入 API 目录
cd api

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，创建默认配置..."
    cat > .env << EOF
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=Asd1988.
DB_NAME=cn2global
JWT_SECRET=cn2global-secret-key-2024
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/api/auth/google/callback
PORT=3000
NODE_ENV=development
EOF
    echo "✅ .env 文件已创建，请编辑并添加 Google OAuth 凭证"
fi

# 检查 node_modules
if [ ! -d node_modules ]; then
    echo "📦 安装依赖..."
    npm install
fi

# 启动服务器
echo "🎯 启动 CN2Global API 服务器..."
echo "📍 访问地址: http://localhost:3000"
echo "📝 注册页面: http://localhost:3000/register_i18n.html"
echo "🔐 登录页面: http://localhost:3000/login_i18n.html"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

node server_i18n.js
