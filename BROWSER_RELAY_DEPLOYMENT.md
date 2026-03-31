# 🚀 CN2Global 完整部署指南 - 使用 Browser Relay

## 📋 部署步骤

### 第 1 步：在腾讯云 WebShell 中打开终端

1. 登录腾讯云控制台
2. 进入轻量应用服务器实例
3. 点击 **WebShell** 按钮
4. 会打开一个浏览器终端

### 第 2 步：下载部署脚本

**在 WebShell 中运行以下命令：**

```bash
# 创建临时目录
mkdir -p /tmp/cn2global_deploy
cd /tmp/cn2global_deploy

# 下载部署脚本
wget https://raw.githubusercontent.com/openclaw/cn2global/main/deploy_all.sh

# 或使用 curl
curl -fsSL https://raw.githubusercontent.com/openclaw/cn2global/main/deploy_all.sh -o deploy_all.sh
```

**如果上面的命令不工作，使用以下方式：**

```bash
# 创建部署脚本
cat > /tmp/deploy_all.sh << 'DEPLOY_SCRIPT_EOF'
# ... 粘贴下面的完整脚本内容 ...
DEPLOY_SCRIPT_EOF
```

### 第 3 步：给脚本执行权限

```bash
chmod +x /tmp/deploy_all.sh
```

### 第 4 步：运行部署脚本

```bash
# 使用 sudo 运行脚本
sudo bash /tmp/deploy_all.sh
```

**脚本会自动：**
- ✅ 更新系统
- ✅ 安装 Node.js 18
- ✅ 安装 MySQL
- ✅ 安装 Nginx
- ✅ 安装 PM2
- ✅ 创建应用目录
- ✅ 安装依赖
- ✅ 配置数据库
- ✅ 配置 Nginx
- ✅ 申请 SSL 证书
- ✅ 启动所有服务

**总耗时：** 10-15 分钟

### 第 5 步：上传网站文件

**在本地电脑上，进入项目目录：**

```bash
cd C:\Users\wangs\.qclaw\workspace\cn2global

# 上传所有文件到服务器
scp -i "C:\Users\wangs\Desktop\cn2g.pem" -r ./* root@119.28.137.229:/var/www/cn2global/
```

**或在 WebShell 中下载文件：**

```bash
# 进入应用目录
cd /var/www/cn2global

# 下载文件（如果你有 GitHub 仓库）
git clone https://github.com/your-repo/cn2global.git .

# 或手动创建文件
# ... 创建 i18n.js, register_i18n.html 等文件 ...
```

### 第 6 步：配置 Google OAuth

**在 WebShell 中编辑 .env 文件：**

```bash
nano /var/www/cn2global/api/.env
```

**找到以下行并填入你的 Google OAuth 凭证：**

```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=https://cn2g.com/api/auth/google/callback
```

**保存文件：**
- 按 Ctrl+O
- 按 Enter
- 按 Ctrl+X

### 第 7 步：重启应用

```bash
pm2 restart cn2global-api
```

### 第 8 步：验证部署

```bash
# 检查应用状态
pm2 status

# 查看应用日志
pm2 logs cn2global-api

# 检查 Nginx 状态
sudo systemctl status nginx

# 检查 MySQL 状态
sudo systemctl status mysql
```

---

## 🔧 常用命令

### 应用管理
```bash
pm2 status              # 查看应用状态
pm2 logs cn2global-api  # 查看应用日志
pm2 restart cn2global-api  # 重启应用
pm2 stop cn2global-api  # 停止应用
pm2 start cn2global-api  # 启动应用
```

### Nginx 管理
```bash
sudo systemctl restart nginx  # 重启 Nginx
sudo systemctl status nginx   # 查看 Nginx 状态
tail -f /var/log/nginx/cn2global_access.log  # 查看日志
sudo nginx -t  # 测试配置
```

### MySQL 管理
```bash
mysql -u root -p  # 连接 MySQL
SHOW DATABASES;   # 查看数据库
USE cn2global;    # 使用数据库
SHOW TABLES;      # 查看表
```

### 文件管理
```bash
ls -la /var/www/cn2global/  # 查看应用文件
cat /var/www/cn2global/api/.env  # 查看 .env 文件
nano /var/www/cn2global/api/.env  # 编辑 .env 文件
```

---

## ✅ 部署完成检查

- [ ] 脚本运行完成
- [ ] 文件已上传
- [ ] Google OAuth 已配置
- [ ] 应用已启动
- [ ] SSL 证书已申请
- [ ] 网站可以访问
- [ ] 功能测试通过

---

## 🌐 访问地址

部署完成后，你可以访问：

- **主页：** https://cn2g.com
- **注册页面：** https://cn2g.com/register_i18n.html
- **登录页面：** https://cn2g.com/login_i18n.html
- **API 文档：** https://cn2g.com/api/support/info

---

## 🚨 故障排查

### 问题 1：脚本执行失败

**症状：** 脚本中途停止

**解决方案：**
```bash
# 查看错误信息
pm2 logs cn2global-api

# 检查网络连接
ping 8.8.8.8

# 重新运行脚本
sudo bash /tmp/deploy_all.sh
```

### 问题 2：SSL 证书申请失败

**症状：** "Certbot failed"

**解决方案：**
```bash
# 检查 DNS 是否已生效
nslookup cn2g.com

# 手动申请证书
sudo certbot certonly --nginx -d cn2g.com -d www.cn2g.com
```

### 问题 3：应用无法启动

**症状：** "pm2 status" 显示 stopped

**解决方案：**
```bash
# 查看日志
pm2 logs cn2global-api

# 检查 .env 文件
cat /var/www/cn2global/api/.env

# 检查 MySQL
sudo systemctl status mysql

# 手动启动
pm2 start /var/www/cn2global/api/server_i18n.js --name cn2global-api
```

### 问题 4：网站无法访问

**症状：** 访问 https://cn2g.com 显示 "无法连接"

**解决方案：**
```bash
# 检查 DNS
nslookup cn2g.com

# 检查 Nginx
sudo systemctl status nginx

# 查看 Nginx 日志
tail -f /var/log/nginx/cn2global_error.log

# 重启 Nginx
sudo systemctl restart nginx
```

---

## 📞 需要帮助？

如果遇到问题，请：
1. 查看服务器日志
2. 检查 DNS 配置
3. 验证 SSL 证书
4. 检查应用状态

---

**最后更新：2026-03-31**
