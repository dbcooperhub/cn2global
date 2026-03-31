#!/bin/bash

# CN2Global 文件上传脚本
# 将本地文件上传到腾讯云服务器

SERVER_IP="119.28.137.229"
SERVER_USER="root"
REMOTE_PATH="/var/www/cn2global"

echo "🚀 CN2Global 文件上传脚本"
echo "=========================="
echo ""
echo "服务器 IP: $SERVER_IP"
echo "远程路径: $REMOTE_PATH"
echo ""

# 检查 SSH 连接
echo "🔍 检查 SSH 连接..."
if ssh -o ConnectTimeout=5 $SERVER_USER@$SERVER_IP "echo 'SSH 连接成功'" > /dev/null 2>&1; then
    echo "✅ SSH 连接成功"
else
    echo "❌ SSH 连接失败"
    echo "请确保："
    echo "  1. 服务器 IP 正确: $SERVER_IP"
    echo "  2. SSH 密钥已配置或密码正确"
    echo "  3. 防火墙允许 SSH 连接"
    exit 1
fi

echo ""
echo "📦 准备上传文件..."

# 创建临时目录
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# 复制文件到临时目录
echo "📋 复制文件..."
cp i18n.js $TEMP_DIR/
cp register_i18n.html $TEMP_DIR/
cp login_i18n.html $TEMP_DIR/
cp index.html $TEMP_DIR/ 2>/dev/null || true
cp style.css $TEMP_DIR/ 2>/dev/null || true

# 创建 api 目录
mkdir -p $TEMP_DIR/api
cp api/server_i18n.js $TEMP_DIR/api/
cp api/package.json $TEMP_DIR/api/ 2>/dev/null || true

echo "✅ 文件已准备"

echo ""
echo "📤 上传文件到服务器..."

# 上传文件
scp -r $TEMP_DIR/* $SERVER_USER@$SERVER_IP:$REMOTE_PATH/

echo "✅ 文件上传完成"

echo ""
echo "🔧 在服务器上安装依赖..."

# 在服务器上安装依赖
ssh $SERVER_USER@$SERVER_IP << 'EOF'
cd /var/www/cn2global/api
npm install
echo "✅ 依赖安装完成"
EOF

echo ""
echo "✅ 所有文件已上传并配置完成！"
echo ""
echo "📍 后续步骤："
echo "  1. 编辑 /var/www/cn2global/api/.env，添加 Google OAuth 凭证"
echo "  2. 运行部署脚本: bash deploy.sh"
echo "  3. 配置 DNS 记录"
echo "  4. 访问 https://cn2g.com"
echo ""
