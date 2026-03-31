# 🚀 CN2Global 快速部署指南 - 使用 SSH 密钥

## 📋 部署信息

- **服务器 IP:** 119.28.137.229
- **用户名:** root
- **SSH 密钥:** ~/Desktop/cn2g.pem
- **密码:** asdfg1988.
- **域名:** cn2g.com

---

## 🎯 3 步快速部署

### 第 1 步：在本地电脑上准备文件

**打开终端/命令行，进入项目目录：**

```bash
cd /path/to/cn2global
```

### 第 2 步：连接到服务器并上传文件

**使用 SSH 密钥连接：**

```bash
# 设置密钥权限（Mac/Linux）
chmod 600 ~/Desktop/cn2g.pem

# 连接到服务器
ssh -i ~/Desktop/cn2g.pem root@119.28.137.229
```

**在服务器上创建应用目录：**

```bash
mkdir -p /var/www/cn2global
cd /var/www/cn2global
```

**在本地电脑上上传文件（新开一个终端）：**

```bash
# 上传所有文件
scp -i ~/Desktop/cn2g.pem -r ./* root@119.28.137.229:/var/www/cn2global/

# 或分别上传
scp -i ~/Desktop/cn2g.pem i18n.js root@119.28.137.229:/var/www/cn2global/
scp -i ~/Desktop/cn2g.pem register_i18n.html root@119.28.137.229:/var/www/cn2global/
scp -i ~/Desktop/cn2g.pem login_i18n.html root@119.28.137.229:/var/www/cn2global/
scp -i ~/Desktop/cn2g.pem index.html root@119.28.137.229:/var/www/cn2global/
scp -i ~/Desktop/cn2g.pem style.css root@119.28.137.229:/var/www/cn2global/
scp -i ~/Desktop/cn2g.pem -r api/ root@119.28.137.229:/var/www/cn2global/
```

### 第 3 步：在服务器上运行部署脚本

**在服务器上运行（SSH 连接中）：**

```bash
# 进入应用目录
cd /var/www/cn2global

# 给脚本执行权限
chmod +x deploy_complete.sh

# 运行部署脚本
sudo bash deploy_complete.sh
```

**脚本会自动：**
- ✅ 更新系统
- ✅ 安装 Node.js 18
- ✅ 安装 MySQL
- ✅ 安装 Nginx
- ✅ 安装 PM2
- ✅ 配置 Nginx 反向代理
- ✅ 申请 SSL 证书
- ✅ 启动应用

**总耗时：** 10-15 分钟

---

## 📝 详细步骤

### 步骤 1：准备 SSH 密钥

**在 Mac/Linux 上：**
```bash
# 设置密钥权限
chmod 600 ~/Desktop/cn2g.pem

# 验证密钥
ssh-keygen -l -f ~/Desktop/cn2g.pem
```

**在 Windows 上（使用 PuTTY）：**
1. 下载 PuTTY: https://www.putty.org/
2. 使用 PuTTYgen 转换密钥格式
3. 使用 PuTTY 连接

**或使用 Windows 10+ 内置 SSH：**
```powershell
# 设置密钥权限
icacls "C:\Users\wangs\Desktop\cn2g.pem" /inheritance:r /grant:r "$env:USERNAME`:F"

# 连接
ssh -i "C:\Users\wangs\Desktop\cn2g.pem" root@119.28.137.229
```

### 步骤 2：连接到服务器

**Mac/Linux：**
```bash
ssh -i ~/Desktop/cn2g.pem root@119.28.137.229
```

**Windows PowerShell：**
```powershell
ssh -i "C:\Users\wangs\Desktop\cn2g.pem" root@119.28.137.229
```

**如果连接失败，使用密码：**
```bash
ssh root@119.28.137.229
# 输入密码: asdfg1988.
```

### 步骤 3：上传文件

**使用 SCP（推荐）：**

```bash
# Mac/Linux
scp -i ~/Desktop/cn2g.pem -r ./* root@119.28.137.229:/var/www/cn2global/

# Windows PowerShell
scp -i "C:\Users\wangs\Desktop\cn2g.pem" -r ./* root@119.28.137.229:/var/www/cn2global/
```

**或使用 SFTP：**

```bash
# 连接 SFTP
sftp -i ~/Desktop/cn2g.pem root@119.28.137.229

# 在 SFTP 中执行
mkdir /var/www/cn2global
cd /var/www/cn2global
put -r ./*
exit
```

### 步骤 4：运行部署脚本

**在 SSH 连接中执行：**

```bash
# 进入应用目录
cd /var/www/cn2global

# 给脚本执行权限
chmod +x deploy_complete.sh

# 运行部署脚本
sudo bash deploy_complete.sh
```

**脚本执行过程中：**
- 会提示输入 sudo 密码（输入：asdfg1988.）
- 会提示申请 SSL 证书，按 Enter 继续
- 会提示输入邮箱地址（输入：admin@cn2g.com）

### 步骤 5：配置 Google OAuth

**编辑 .env 文件：**

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

**重启应用：**

```bash
pm2 restart cn2global-api
```

---

## ✅ 验证部署

### 1. 检查应用状态

```bash
pm2 status
# 应该看到 cn2global-api 处于 online 状态
```

### 2. 检查日志

```bash
pm2 logs cn2global-api
# 应该看到应用启动日志
```

### 3. 检查 Nginx

```bash
sudo systemctl status nginx
# 应该看到 active (running)
```

### 4. 检查 MySQL

```bash
sudo systemctl status mysql
# 应该看到 active (running)
```

### 5. 访问网站

- 打开浏览器
- 访问 **https://cn2g.com**
- 应该看到 CN2Global 主页

---

## 🔧 常用命令

### 应用管理

```bash
# 查看应用状态
pm2 status

# 查看应用日志
pm2 logs cn2global-api

# 重启应用
pm2 restart cn2global-api

# 停止应用
pm2 stop cn2global-api

# 启动应用
pm2 start cn2global-api

# 删除应用
pm2 delete cn2global-api
```

### Nginx 管理

```bash
# 重启 Nginx
sudo systemctl restart nginx

# 查看 Nginx 状态
sudo systemctl status nginx

# 查看 Nginx 日志
tail -f /var/log/nginx/cn2global_access.log

# 测试 Nginx 配置
sudo nginx -t
```

### MySQL 管理

```bash
# 连接 MySQL
mysql -u root -p

# 查看数据库
SHOW DATABASES;

# 使用数据库
USE cn2global;

# 查看表
SHOW TABLES;

# 查看用户
SELECT * FROM users;
```

### 文件管理

```bash
# 查看应用文件
ls -la /var/www/cn2global/

# 查看 .env 文件
cat /var/www/cn2global/api/.env

# 编辑 .env 文件
nano /var/www/cn2global/api/.env

# 查看部署日志
cat /var/log/nginx/cn2global_access.log
```

---

## 🚨 故障排查

### 问题 1：SSH 连接失败

**症状：** "Permission denied (publickey)"

**解决方案：**
1. 检查密钥文件权限：`chmod 600 ~/Desktop/cn2g.pem`
2. 检查密钥文件是否存在
3. 尝试使用密码连接：`ssh root@119.28.137.229`

### 问题 2：SCP 上传失败

**症状：** "Permission denied"

**解决方案：**
1. 检查密钥文件权限
2. 检查远程目录是否存在
3. 尝试手动创建目录：`ssh -i ~/Desktop/cn2g.pem root@119.28.137.229 "mkdir -p /var/www/cn2global"`

### 问题 3：部署脚本失败

**症状：** 脚本中途停止

**解决方案：**
1. 查看错误信息
2. 检查网络连接
3. 尝试重新运行脚本
4. 查看日志：`pm2 logs cn2global-api`

### 问题 4：SSL 证书申请失败

**症状：** "Certbot failed"

**解决方案：**
1. 检查 DNS 是否已生效
2. 检查防火墙是否开放 80 和 443 端口
3. 手动申请证书：`sudo certbot certonly --nginx -d cn2g.com -d www.cn2g.com`

### 问题 5：应用无法启动

**症状：** "pm2 status" 显示 stopped

**解决方案：**
1. 查看日志：`pm2 logs cn2global-api`
2. 检查 .env 文件配置
3. 检查 MySQL 是否运行
4. 手动启动：`pm2 start /var/www/cn2global/api/server_i18n.js --name cn2global-api`

---

## 📞 需要帮助？

如果遇到问题，请：
1. 查看服务器日志
2. 检查 DNS 配置
3. 验证 SSL 证书
4. 检查应用状态

---

**最后更新：2026-03-31**
