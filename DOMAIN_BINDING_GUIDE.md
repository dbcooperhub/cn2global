# 🎉 CN2Global 域名绑定和部署方案 - 完整指南

## 📍 部署信息

| 项目 | 信息 |
|------|------|
| 域名 | cn2g.com |
| 服务器 IP | 119.28.137.229 |
| 云平台 | 腾讯云轻量应用服务器 |
| 域名注册商 | 阿里云 |
| 操作系统 | Linux (Ubuntu/CentOS) |
| 应用框架 | Node.js + Express |
| 数据库 | MySQL |
| Web 服务器 | Nginx |
| SSL 证书 | Let's Encrypt (免费) |

---

## 🚀 快速部署（3 步）

### 第 1 步：配置 DNS（5 分钟）

**在阿里云域名管理中：**

1. 登录 https://dc.console.aliyun.com/
2. 找到 **cn2g.com** 域名
3. 点击 **管理** → **DNS 解析**
4. 添加以下 A 记录：

| 主机记录 | 记录类型 | 记录值 | TTL |
|---------|---------|--------|-----|
| @ | A | 119.28.137.229 | 600 |
| www | A | 119.28.137.229 | 600 |

5. 等待 DNS 生效（5-30 分钟）

**验证 DNS：**
```bash
nslookup cn2g.com
# 应该看到：119.28.137.229
```

### 第 2 步：连接服务器并上传文件（10 分钟）

**连接到服务器：**
```bash
ssh root@119.28.137.229
```

**创建应用目录：**
```bash
mkdir -p /var/www/cn2global
cd /var/www/cn2global
```

**上传文件（在本地电脑运行）：**
```bash
scp -r ./cn2global/* root@119.28.137.229:/var/www/cn2global/
```

### 第 3 步：运行自动化部署脚本（15 分钟）

**在服务器上运行：**
```bash
cd /var/www/cn2global
chmod +x deploy.sh
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

**总耗时：** 约 30 分钟

---

## 📋 详细部署步骤

### 步骤 1：DNS 配置

#### 1.1 登录阿里云
- 访问：https://dc.console.aliyun.com/
- 输入账户和密码登录

#### 1.2 进入域名管理
- 在左侧菜单找到 **域名列表**
- 找到 **cn2g.com**
- 点击 **管理**

#### 1.3 配置 DNS 解析
- 点击 **DNS 解析**
- 点击 **添加记录**
- 填写以下信息：
  - 记录类型：**A**
  - 主机记录：**@**
  - 记录值：**119.28.137.229**
  - TTL：**600**
- 点击 **确定**

#### 1.4 添加 www 记录
- 重复上述步骤
- 主机记录改为：**www**
- 其他信息相同

#### 1.5 验证 DNS
```bash
# 等待 5-30 分钟后运行
nslookup cn2g.com

# 应该看到：
# Name: cn2g.com
# Address: 119.28.137.229
```

### 步骤 2：服务器连接

#### 2.1 获取 SSH 密钥或密码
- 登录腾讯云控制台
- 找到轻量应用服务器实例
- 获取 SSH 密钥或重置密码

#### 2.2 连接服务器
```bash
# 使用密码连接
ssh root@119.28.137.229

# 或使用 SSH 密钥
ssh -i /path/to/key.pem root@119.28.137.229
```

#### 2.3 验证连接
```bash
# 应该看到服务器提示符
root@server:~#
```

### 步骤 3：上传文件

#### 3.1 创建应用目录
```bash
mkdir -p /var/www/cn2global
cd /var/www/cn2global
```

#### 3.2 上传文件（在本地电脑运行）
```bash
# 进入 cn2global 项目目录
cd /path/to/cn2global

# 上传所有文件
scp -r ./* root@119.28.137.229:/var/www/cn2global/

# 或使用 FTP/SFTP 工具上传
```

#### 3.3 验证文件
```bash
# 在服务器上运行
ls -la /var/www/cn2global/

# 应该看到：
# i18n.js
# register_i18n.html
# login_i18n.html
# api/
# deploy.sh
# ...
```

### 步骤 4：运行部署脚本

#### 4.1 给脚本执行权限
```bash
chmod +x /var/www/cn2global/deploy.sh
```

#### 4.2 运行脚本
```bash
sudo bash /var/www/cn2global/deploy.sh
```

#### 4.3 按照提示操作
- 脚本会自动安装所有依赖
- 当提示申请 SSL 证书时，按 Enter 继续
- 输入邮箱地址（用于证书通知）

#### 4.4 等待完成
- 脚本运行时间：10-15 分钟
- 完成后会显示 "✅ 部署完成！"

### 步骤 5：配置 Google OAuth

#### 5.1 编辑 .env 文件
```bash
nano /var/www/cn2global/api/.env
```

#### 5.2 填入 Google OAuth 凭证
```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=https://cn2g.com/api/auth/google/callback
```

#### 5.3 保存文件
- 按 Ctrl+O
- 按 Enter
- 按 Ctrl+X

#### 5.4 重启应用
```bash
pm2 restart cn2global-api
```

---

## ✅ 验证部署

### 1. DNS 验证
```bash
nslookup cn2g.com
# 应该返回：119.28.137.229
```

### 2. 网站访问
- 打开浏览器
- 访问 **https://cn2g.com**
- 应该看到 CN2Global 主页

### 3. 功能测试
- 访问注册页面：https://cn2g.com/register_i18n.html
- 访问登录页面：https://cn2g.com/login_i18n.html
- 测试语言切换
- 测试 Google OAuth 按钮

### 4. API 测试
```bash
curl -X POST https://cn2g.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"country":"CN","phone":"+8613800000000","password":"Test123456"}'
```

### 5. 服务器状态
```bash
# 检查应用状态
pm2 status

# 应该看到 cn2global-api 处于 online 状态
```

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
```

### Nginx 管理
```bash
# 重启 Nginx
sudo systemctl restart nginx

# 查看 Nginx 状态
sudo systemctl status nginx

# 查看 Nginx 日志
tail -f /var/log/nginx/cn2global_access.log
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
```

---

## 🚨 故障排查

### 问题 1：DNS 未生效
**症状：** 访问 cn2g.com 显示 "无法连接"

**解决方案：**
1. 检查 DNS 配置是否正确
2. 等待 DNS 缓存过期（5-30 分钟）
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
2. 检查 Nginx 配置中的证书路径
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

## 📊 部署完成检查

- [ ] DNS 已配置
- [ ] 文件已上传
- [ ] 部署脚本已运行
- [ ] Google OAuth 已配置
- [ ] 应用已启动
- [ ] SSL 证书已申请
- [ ] 网站可以访问
- [ ] 功能测试通过
- [ ] API 测试通过

---

## 📞 后续支持

### 定期维护
- 每周检查服务器状态
- 每月检查 SSL 证书有效期
- 定期备份数据库

### 监控和告警
- 配置服务器监控
- 设置告警规则
- 定期查看日志

### 更新和升级
- 定期更新系统
- 定期更新依赖包
- 定期更新应用代码

---

## 📝 相关文档

- **DNS_DEPLOYMENT_GUIDE.md** - DNS 和部署详细指南
- **DEPLOYMENT_CHECKLIST.md** - 部署检查清单
- **DEPLOYMENT_GUIDE.md** - 完整部署指南
- **QUICK_REFERENCE.md** - 快速参考卡

---

**部署状态：✅ 准备就绪**

**下一步：**
1. 配置 DNS 记录
2. 连接服务器
3. 上传文件
4. 运行部署脚本
5. 配置 Google OAuth
6. 验证部署

**预计总耗时：** 30-45 分钟

---

**最后更新：2026-03-31**
