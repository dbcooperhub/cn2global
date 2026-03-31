# 🚀 CN2Global 一键部署命令

## 📋 在腾讯云 WebShell 中直接运行以下命令

### 第 1 步：复制以下完整的部署脚本

```bash
#!/bin/bash
set -e

echo "🚀 CN2Global 完整一键部署脚本"
echo "======================================"

# 检查 root 权限
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 请使用 root 权限运行此脚本"
    exit 1
fi

# 更新系统
echo "📋 更新系统..."
apt-get update && apt-get upgrade -y

# 安装依赖
echo "📋 安装依赖..."
apt-get install -y curl wget git build-essential

# 安装 Node.js 18
echo "📋 安装 Node.js 18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# 安装 MySQL
echo "📋 安装 MySQL..."
apt-get install -y mysql-server

# 安装 Nginx
echo "📋 安装 Nginx..."
apt-get install -y nginx

# 安装 PM2
echo "📋 安装 PM2..."
npm install -g pm2

# 创建应用目录
echo "📋 创建应用目录..."
mkdir -p /var/www/cn2global/api
cd /var/www/cn2global

# 创建 package.json
echo "📋 创建 package.json..."
cat > api/package.json << 'EOF'
{
  "name": "cn2global-api",
  "version": "1.0.0",
  "description": "CN2Global API Server",
  "main": "server_i18n.js",
  "scripts": {
    "start": "node server_i18n.js"
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

# 安装依赖
echo "📋 安装 Node.js 依赖..."
cd api && npm install

# 创建 .env 文件
echo "📋 创建 .env 文件..."
cat > .env << 'EOF'
DB_HOST=localhost
DB_USER=cn2global
DB_PASSWORD=cn2global_password_2024
DB_NAME=cn2global
JWT_SECRET=cn2global-secret-key-2024
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://cn2g.com/api/auth/google/callback
PORT=3000
NODE_ENV=production
EOF

# 配置 MySQL
echo "📋 配置 MySQL..."
mysql -u root << MYSQL_SCRIPT
CREATE DATABASE IF NOT EXISTS cn2global CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'cn2global'@'localhost' IDENTIFIED BY 'cn2global_password_2024';
GRANT ALL PRIVILEGES ON cn2global.* TO 'cn2global'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

# 配置 Nginx
echo "📋 配置 Nginx..."
cat > /etc/nginx/sites-available/cn2global << 'EOF'
server {
    listen 80;
    server_name cn2g.com www.cn2g.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cn2g.com www.cn2g.com;
    ssl_certificate /etc/letsencrypt/live/cn2g.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/cn2g.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    access_log /var/log/nginx/cn2global_access.log;
    error_log /var/log/nginx/cn2global_error.log;

    location / {
        root /var/www/cn2global;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/cn2global /etc/nginx/sites-enabled/cn2global
rm -f /etc/nginx/sites-enabled/default
nginx -t

# 安装 Certbot
echo "📋 安装 Certbot..."
apt-get install -y certbot python3-certbot-nginx

# 申请 SSL 证书
echo "📋 申请 SSL 证书..."
echo "⚠️  请确保 DNS 已指向此服务器 IP: 119.28.137.229"
read -p "按 Enter 继续申请 SSL 证书..."
certbot certonly --nginx -d cn2g.com -d www.cn2g.com --non-interactive --agree-tos -m admin@cn2g.com

# 启动服务
echo "📋 启动服务..."
systemctl restart nginx
systemctl enable nginx

cd /var/www/cn2global/api
pm2 start server_i18n.js --name "cn2global-api"
pm2 startup
pm2 save

# 配置防火墙
echo "📋 配置防火墙..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo ""
echo "✅ 部署完成！"
echo ""
echo "📍 访问地址:"
echo "  - 主页: https://cn2g.com"
echo "  - 注册: https://cn2g.com/register_i18n.html"
echo "  - 登录: https://cn2g.com/login_i18n.html"
echo ""
echo "📝 后续步骤:"
echo "  1. 编辑 /var/www/cn2global/api/.env，添加 Google OAuth 凭证"
echo "  2. 重启应用: pm2 restart cn2global-api"
echo "  3. 查看日志: pm2 logs cn2global-api"
echo ""
```

### 第 2 步：在腾讯云 WebShell 中运行

1. **打开腾讯云 WebShell**
   - 登录腾讯云控制台
   - 进入轻量应用服务器实例
   - 点击 **WebShell** 按钮

2. **复制上面的完整脚本**

3. **粘贴到 WebShell 中**

4. **按 Enter 运行**

5. **等待部署完成（10-15 分钟）**

---

## 🎯 简化版本（如果上面的脚本太长）

**如果你想要一个更简单的版本，可以分步运行：**

```bash
# 第 1 步：更新系统
sudo apt-get update && sudo apt-get upgrade -y

# 第 2 步：安装依赖
sudo apt-get install -y curl wget git build-essential

# 第 3 步：安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 第 4 步：安装 MySQL
sudo apt-get install -y mysql-server

# 第 5 步：安装 Nginx
sudo apt-get install -y nginx

# 第 6 步：安装 PM2
sudo npm install -g pm2

# 第 7 步：创建应用目录
sudo mkdir -p /var/www/cn2global/api
cd /var/www/cn2global

# 第 8 步：配置 MySQL
sudo mysql -u root << 'EOF'
CREATE DATABASE IF NOT EXISTS cn2global CHARACTER SET utf8mb4;
CREATE USER IF NOT EXISTS 'cn2global'@'localhost' IDENTIFIED BY 'cn2global_password_2024';
GRANT ALL PRIVILEGES ON cn2global.* TO 'cn2global'@'localhost';
FLUSH PRIVILEGES;
EOF

# 第 9 步：配置 Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx

# 第 10 步：安装 Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# 第 11 步：申请 SSL 证书
sudo certbot certonly --nginx -d cn2g.com -d www.cn2g.com --non-interactive --agree-tos -m admin@cn2g.com

# 第 12 步：启动应用
cd /var/www/cn2global/api
sudo pm2 start server_i18n.js --name "cn2global-api"
sudo pm2 startup
sudo pm2 save

echo "✅ 部署完成！"
```

---

## 📝 后续步骤

### 1. 上传网站文件

**在本地电脑上运行：**

```bash
cd C:\Users\wangs\.qclaw\workspace\cn2global

# 上传所有文件
scp -i "C:\Users\wangs\Desktop\cn2g.pem" -r ./* root@119.28.137.229:/var/www/cn2global/
```

### 2. 配置 Google OAuth

**在 WebShell 中编辑 .env 文件：**

```bash
sudo nano /var/www/cn2global/api/.env

# 找到以下行并填入你的 Google OAuth 凭证：
# GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
# GOOGLE_CLIENT_SECRET=your-client-secret
# GOOGLE_REDIRECT_URI=https://cn2g.com/api/auth/google/callback
```

### 3. 重启应用

```bash
pm2 restart cn2global-api
```

### 4. 验证部署

```bash
# 检查应用状态
pm2 status

# 查看日志
pm2 logs cn2global-api

# 访问网站
# https://cn2g.com
```

---

**现在就在腾讯云 WebShell 中运行上面的脚本吧！** 🚀
