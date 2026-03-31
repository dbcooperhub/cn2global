#!/bin/bash

# CN2Global 自动化部署脚本 - 腾讯云轻量应用服务器
# 使用方法：bash deploy.sh

set -e

echo "🚀 CN2Global 自动化部署脚本"
echo "============================"
echo ""
echo "服务器 IP: 119.28.137.229"
echo "域名: cn2g.com"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查是否为 root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ 请使用 root 权限运行此脚本${NC}"
    echo "使用: sudo bash deploy.sh"
    exit 1
fi

echo -e "${YELLOW}📋 第 1 步：更新系统${NC}"
apt-get update
apt-get upgrade -y

echo -e "${YELLOW}📋 第 2 步：安装依赖${NC}"
apt-get install -y curl wget git build-essential

echo -e "${YELLOW}📋 第 3 步：安装 Node.js 18${NC}"
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

echo "✅ Node.js 版本: $(node -v)"
echo "✅ npm 版本: $(npm -v)"

echo -e "${YELLOW}📋 第 4 步：安装 MySQL${NC}"
apt-get install -y mysql-server

echo "✅ MySQL 已安装"

echo -e "${YELLOW}📋 第 5 步：安装 Nginx${NC}"
apt-get install -y nginx

echo "✅ Nginx 已安装"

echo -e "${YELLOW}📋 第 6 步：安装 PM2（进程管理）${NC}"
npm install -g pm2

echo "✅ PM2 已安装"

echo -e "${YELLOW}📋 第 7 步：创建应用目录${NC}"
mkdir -p /var/www/cn2global
cd /var/www/cn2global

echo -e "${YELLOW}📋 第 8 步：下载 CN2Global 文件${NC}"
# 这里应该从你的源下载文件
# 暂时创建目录结构
mkdir -p api public src

echo -e "${YELLOW}📋 第 9 步：创建 package.json${NC}"
cat > api/package.json << 'EOF'
{
  "name": "cn2global-api",
  "version": "1.0.0",
  "description": "CN2Global API Server",
  "main": "server_i18n.js",
  "scripts": {
    "start": "node server_i18n.js",
    "dev": "nodemon server_i18n.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mysql2": "^3.6.0",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.0",
    "cors": "^2.8.5",
    "express-validator": "^7.0.0",
    "dotenv": "^16.0.3",
    "axios": "^1.4.0"
  }
}
EOF

echo "✅ package.json 已创建"

echo -e "${YELLOW}📋 第 10 步：安装 Node.js 依赖${NC}"
cd api
npm install

echo -e "${YELLOW}📋 第 11 步：创建 .env 文件${NC}"
cat > .env << 'EOF'
# 数据库配置
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=cn2global_password_2024
DB_NAME=cn2global

# JWT 配置
JWT_SECRET=cn2global-secret-key-2024-change-in-production

# Google OAuth 配置
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://cn2g.com/api/auth/google/callback

# 服务器配置
PORT=3000
NODE_ENV=production
EOF

echo "✅ .env 文件已创建"
echo -e "${YELLOW}⚠️  请编辑 .env 文件，添加 Google OAuth 凭证${NC}"

echo -e "${YELLOW}📋 第 12 步：配置 MySQL${NC}"
mysql -u root << MYSQL_SCRIPT
CREATE DATABASE IF NOT EXISTS cn2global CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'cn2global'@'localhost' IDENTIFIED BY 'cn2global_password_2024';
GRANT ALL PRIVILEGES ON cn2global.* TO 'cn2global'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

echo "✅ MySQL 数据库已创建"

echo -e "${YELLOW}📋 第 13 步：配置 Nginx${NC}"
cat > /etc/nginx/sites-available/cn2global << 'EOF'
server {
    listen 80;
    server_name cn2g.com www.cn2g.com;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cn2g.com www.cn2g.com;

    # SSL 证书（稍后配置）
    ssl_certificate /etc/letsencrypt/live/cn2g.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/cn2g.com/privkey.pem;

    # SSL 配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 日志
    access_log /var/log/nginx/cn2global_access.log;
    error_log /var/log/nginx/cn2global_error.log;

    # 静态文件
    location / {
        root /var/www/cn2global;
        try_files $uri $uri/ /index.html;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }

    # API 代理
    location /api {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
EOF

# 启用站点
ln -sf /etc/nginx/sites-available/cn2global /etc/nginx/sites-enabled/cn2global
rm -f /etc/nginx/sites-enabled/default

# 测试 Nginx 配置
nginx -t

echo "✅ Nginx 配置已完成"

echo -e "${YELLOW}📋 第 14 步：安装 Certbot（Let's Encrypt）${NC}"
apt-get install -y certbot python3-certbot-nginx

echo "✅ Certbot 已安装"

echo -e "${YELLOW}📋 第 15 步：申请 SSL 证书${NC}"
echo -e "${YELLOW}⚠️  请确保域名 DNS 已指向此服务器 IP: 119.28.137.229${NC}"
echo ""
echo "按 Enter 继续申请 SSL 证书..."
read

certbot certonly --nginx -d cn2g.com -d www.cn2g.com --non-interactive --agree-tos -m admin@cn2g.com

echo "✅ SSL 证书已申请"

echo -e "${YELLOW}📋 第 16 步：启动 Nginx${NC}"
systemctl restart nginx
systemctl enable nginx

echo "✅ Nginx 已启动"

echo -e "${YELLOW}📋 第 17 步：启动 Node.js 应用${NC}"
cd /var/www/cn2global/api
pm2 start server_i18n.js --name "cn2global-api"
pm2 startup
pm2 save

echo "✅ Node.js 应用已启动"

echo ""
echo -e "${GREEN}✅ 部署完成！${NC}"
echo ""
echo "📍 访问地址："
echo "  - 主页: https://cn2g.com"
echo "  - 注册: https://cn2g.com/register_i18n.html"
echo "  - 登录: https://cn2g.com/login_i18n.html"
echo ""
echo "📝 后续步骤："
echo "  1. 编辑 /var/www/cn2global/api/.env，添加 Google OAuth 凭证"
echo "  2. 重启应用: pm2 restart cn2global-api"
echo "  3. 查看日志: pm2 logs cn2global-api"
echo ""
echo "🔐 SSL 证书自动续期已配置"
echo ""
