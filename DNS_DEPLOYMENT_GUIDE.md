# CN2Global 域名绑定和 DNS 配置指南

## 🎯 目标
将域名 **cn2g.com** 绑定到服务器 IP **119.28.137.229**，使访问 https://cn2g.com 可以直接访问网站。

---

## 📋 配置步骤

### 第 1 步：在阿里云域名管理中配置 DNS

#### 1.1 登录阿里云域名控制台
- 访问：https://dc.console.aliyun.com/
- 登录你的阿里云账户

#### 1.2 找到 cn2g.com 域名
- 在域名列表中找到 **cn2g.com**
- 点击 **管理** 或 **解析**

#### 1.3 添加 A 记录
在 DNS 解析页面，添加以下记录：

| 记录类型 | 主机记录 | 记录值 | TTL |
|---------|---------|--------|-----|
| A | @ | 119.28.137.229 | 600 |
| A | www | 119.28.137.229 | 600 |
| CNAME | www | cn2g.com | 600 |

**详细步骤：**
1. 点击 **添加记录**
2. 记录类型选择 **A**
3. 主机记录输入 **@**（表示根域名）
4. 记录值输入 **119.28.137.229**
5. TTL 保持默认 **600**
6. 点击 **确定**

重复上述步骤，添加 www 记录。

#### 1.4 验证 DNS 配置
```bash
# 在本地电脑运行以下命令验证
nslookup cn2g.com
# 或
dig cn2g.com

# 应该看到：
# cn2g.com. 600 IN A 119.28.137.229
```

---

### 第 2 步：在服务器上部署应用

#### 2.1 连接到服务器
```bash
# 使用 SSH 连接
ssh root@119.28.137.229

# 或在腾讯云控制台使用 WebShell
```

#### 2.2 下载部署脚本
```bash
# 创建应用目录
mkdir -p /var/www/cn2global
cd /var/www/cn2global

# 下载部署脚本
wget https://your-domain.com/deploy.sh
# 或手动上传 deploy.sh 文件
```

#### 2.3 运行部署脚本
```bash
# 给脚本执行权限
chmod +x deploy.sh

# 运行部署脚本（需要 root 权限）
sudo bash deploy.sh
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

#### 2.4 上传网站文件
```bash
# 上传前端文件到 /var/www/cn2global
scp -r /path/to/cn2global/* root@119.28.137.229:/var/www/cn2global/

# 或使用 FTP/SFTP 工具上传
```

---

### 第 3 步：配置 Google OAuth

#### 3.1 编辑 .env 文件
```bash
# 连接到服务器
ssh root@119.28.137.229

# 编辑 .env 文件
nano /var/www/cn2global/api/.env

# 找到以下行，填入你的 Google OAuth 凭证：
# GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
# GOOGLE_CLIENT_SECRET=your-google-client-secret
# GOOGLE_REDIRECT_URI=https://cn2g.com/api/auth/google/callback
```

#### 3.2 重启应用
```bash
pm2 restart cn2global-api
```

---

### 第 4 步：验证部署

#### 4.1 检查 DNS 解析
```bash
# 等待 DNS 生效（通常 5-30 分钟）
nslookup cn2g.com

# 应该看到：
# Name: cn2g.com
# Address: 119.28.137.229
```

#### 4.2 访问网站
- 打开浏览器
- 访问 **https://cn2g.com**
- 应该看到 CN2Global 主页

#### 4.3 测试功能
- 访问注册页面：https://cn2g.com/register_i18n.html
- 访问登录页面：https://cn2g.com/login_i18n.html
- 测试语言切换
- 测试 Google OAuth

#### 4.4 查看服务器日志
```bash
# 查看 Nginx 日志
tail -f /var/log/nginx/cn2global_access.log

# 查看应用日志
pm2 logs cn2global-api

# 查看 MySQL 日志
tail -f /var/log/mysql/error.log
```

---

## 🔐 SSL 证书配置

### 自动续期
```bash
# 设置 Certbot 自动续期
sudo certbot renew --dry-run

# 查看证书信息
sudo certbot certificates
```

### 手动续期
```bash
sudo certbot renew --force-renewal
```

---

## 🚀 常用命令

### 应用管理
```bash
# 启动应用
pm2 start cn2global-api

# 停止应用
pm2 stop cn2global-api

# 重启应用
pm2 restart cn2global-api

# 查看应用状态
pm2 status

# 查看应用日志
pm2 logs cn2global-api

# 删除应用
pm2 delete cn2global-api
```

### Nginx 管理
```bash
# 启动 Nginx
sudo systemctl start nginx

# 停止 Nginx
sudo systemctl stop nginx

# 重启 Nginx
sudo systemctl restart nginx

# 重新加载配置
sudo systemctl reload nginx

# 查看状态
sudo systemctl status nginx

# 测试配置
sudo nginx -t
```

### MySQL 管理
```bash
# 启动 MySQL
sudo systemctl start mysql

# 停止 MySQL
sudo systemctl stop mysql

# 重启 MySQL
sudo systemctl restart mysql

# 连接 MySQL
mysql -u root -p

# 查看数据库
SHOW DATABASES;

# 使用数据库
USE cn2global;

# 查看表
SHOW TABLES;
```

---

## 🔧 故障排查

### 问题 1：DNS 未生效
**症状：** 访问 cn2g.com 显示 "无法连接"  
**解决方案：**
1. 检查 DNS 配置是否正确
2. 等待 DNS 缓存过期（通常 5-30 分钟）
3. 清除本地 DNS 缓存：
   ```bash
   # Windows
   ipconfig /flushdns
   
   # Mac
   sudo dscacheutil -flushcache
   
   # Linux
   sudo systemctl restart systemd-resolved
   ```

### 问题 2：SSL 证书错误
**症状：** 浏览器显示 "证书不受信任"  
**解决方案：**
1. 检查证书是否已申请：`sudo certbot certificates`
2. 检查 Nginx 配置中的证书路径是否正确
3. 重新申请证书：`sudo certbot renew --force-renewal`

### 问题 3：应用无法启动
**症状：** 访问 API 返回 502 Bad Gateway  
**解决方案：**
1. 检查应用状态：`pm2 status`
2. 查看应用日志：`pm2 logs cn2global-api`
3. 检查 .env 文件配置
4. 检查 MySQL 是否运行：`sudo systemctl status mysql`
5. 重启应用：`pm2 restart cn2global-api`

### 问题 4：数据库连接失败
**症状：** 应用日志显示 "ECONNREFUSED"  
**解决方案：**
1. 检查 MySQL 是否运行：`sudo systemctl status mysql`
2. 检查 .env 中的数据库凭证
3. 检查数据库是否存在：`mysql -u root -p -e "SHOW DATABASES;"`
4. 重启 MySQL：`sudo systemctl restart mysql`

---

## 📊 监控和维护

### 定期检查
```bash
# 检查磁盘空间
df -h

# 检查内存使用
free -h

# 检查 CPU 使用
top

# 检查进程
ps aux | grep node
```

### 日志轮转
```bash
# 配置 Nginx 日志轮转
sudo nano /etc/logrotate.d/nginx

# 配置应用日志轮转
pm2 install pm2-logrotate
```

### 备份
```bash
# 备份数据库
mysqldump -u root -p cn2global > /backup/cn2global_$(date +%Y%m%d).sql

# 备份应用文件
tar -czf /backup/cn2global_$(date +%Y%m%d).tar.gz /var/www/cn2global
```

---

## 📞 技术支持

如有问题，请：
1. 查看服务器日志
2. 检查 DNS 配置
3. 验证 SSL 证书
4. 检查应用状态

---

**最后更新：2026-03-31**
