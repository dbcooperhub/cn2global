# 🚀 CN2Global 完整部署指南 - 最终版本

## 📋 你的账户信息

| 项目 | 信息 |
|------|------|
| **腾讯云账户** | kmp@163.com |
| **服务器 IP** | 119.28.137.229 |
| **用户名** | root |
| **SSH 密钥** | ~/Desktop/cn2g.pem |
| **密码** | asdfg1988. |
| **域名** | cn2g.com |

---

## 🎯 部署步骤（3 步）

### 第 1 步：连接到服务器

**在你的本地电脑上打开 PowerShell 或 Terminal，运行：**

```bash
# 使用 SSH 密钥连接
ssh -i "C:\Users\wangs\Desktop\cn2g.pem" root@119.28.137.229

# 如果密钥不工作，使用密码连接
ssh root@119.28.137.229
# 输入密码：asdfg1988.
```

**连接成功后，你会看到：**
```
root@server:~#
```

### 第 2 步：下载并运行部署脚本

**在服务器上运行以下命令：**

```bash
# 创建临时目录
mkdir -p /tmp/cn2global_deploy
cd /tmp/cn2global_deploy

# 下载部署脚本
wget https://raw.githubusercontent.com/openclaw/cn2global/main/deploy_final.sh

# 或使用 curl
curl -fsSL https://raw.githubusercontent.com/openclaw/cn2global/main/deploy_final.sh -o deploy_final.sh

# 给脚本执行权限
chmod +x deploy_final.sh

# 运行部署脚本
sudo bash deploy_final.sh
```

**如果上面的下载不工作，使用以下方式：**

```bash
# 创建脚本文件
cat > /tmp/deploy_final.sh << 'DEPLOY_SCRIPT_EOF'
# ... 粘贴下面的完整脚本内容 ...
DEPLOY_SCRIPT_EOF

# 运行脚本
sudo bash /tmp/deploy_final.sh
```

### 第 3 步：上传网站文件

**脚本运行完成后，在本地电脑上运行：**

```bash
# 进入项目目录
cd C:\Users\wangs\.qclaw\workspace\cn2global

# 上传所有文件到服务器
scp -i "C:\Users\wangs\Desktop\cn2g.pem" -r ./* root@119.28.137.229:/var/www/cn2global/

# 或分别上传关键文件
scp -i "C:\Users\wangs\Desktop\cn2g.pem" i18n.js root@119.28.137.229:/var/www/cn2global/
scp -i "C:\Users\wangs\Desktop\cn2g.pem" register_i18n.html root@119.28.137.229:/var/www/cn2global/
scp -i "C:\Users\wangs\Desktop\cn2g.pem" login_i18n.html root@119.28.137.229:/var/www/cn2global/
scp -i "C:\Users\wangs\Desktop\cn2g.pem" index.html root@119.28.137.229:/var/www/cn2global/
scp -i "C:\Users\wangs\Desktop\cn2g.pem" style.css root@119.28.137.229:/var/www/cn2global/
scp -i "C:\Users\wangs\Desktop\cn2g.pem" -r api/ root@119.28.137.229:/var/www/cn2global/
```

---

## 📝 后续配置

### 1. 配置 Google OAuth

**在服务器上编辑 .env 文件：**

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

### 2. 重启应用

```bash
pm2 restart cn2global-api
```

### 3. 验证部署

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

## 🌐 访问网站

部署完成后，你可以访问：

- **主页：** https://cn2g.com
- **注册页面：** https://cn2g.com/register_i18n.html
- **登录页面：** https://cn2g.com/login_i18n.html
- **API 文档：** https://cn2g.com/api/support/info

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

## 🚨 故障排查

### 问题 1：SSH 连接失败

**症状：** "Permission denied (publickey)"

**解决方案：**
```bash
# 检查密钥文件权限
chmod 600 ~/Desktop/cn2g.pem

# 尝试使用密码连接
ssh root@119.28.137.229
# 输入密码：asdfg1988.
```

### 问题 2：脚本执行失败

**症状：** 脚本中途停止

**解决方案：**
```bash
# 查看错误信息
pm2 logs cn2global-api

# 检查网络连接
ping 8.8.8.8

# 重新运行脚本
sudo bash /tmp/deploy_final.sh
```

### 问题 3：SSL 证书申请失败

**症状：** "Certbot failed"

**解决方案：**
```bash
# 检查 DNS 是否已生效
nslookup cn2g.com

# 手动申请证书
sudo certbot certonly --nginx -d cn2g.com -d www.cn2g.com
```

### 问题 4：应用无法启动

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

---

## 📊 部署完成检查

- [ ] SSH 连接成功
- [ ] 部署脚本运行完成
- [ ] 文件已上传
- [ ] Google OAuth 已配置
- [ ] 应用已启动
- [ ] SSL 证书已申请
- [ ] 网站可以访问
- [ ] 功能测试通过

---

## 📞 需要帮助？

如果遇到问题，请：
1. 查看服务器日志
2. 检查 DNS 配置
3. 验证 SSL 证书
4. 检查应用状态

---

**最后更新：2026-03-31**

祝你部署顺利！🚀
