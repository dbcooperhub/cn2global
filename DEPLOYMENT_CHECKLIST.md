# 🚀 CN2Global 部署检查清单

## 📋 部署前准备

### 1. 域名配置
- [ ] 域名 cn2g.com 已在阿里云注册
- [ ] 域名已实名认证
- [ ] 域名已激活

### 2. 服务器准备
- [ ] 腾讯云轻量应用服务器已创建
- [ ] 服务器 IP: **119.28.137.229**
- [ ] 服务器操作系统: Linux (Ubuntu/CentOS)
- [ ] 服务器已启动
- [ ] 防火墙已开放 80 和 443 端口

### 3. 本地准备
- [ ] 已下载所有 CN2Global 文件
- [ ] 已安装 SSH 客户端
- [ ] 已配置 SSH 密钥或密码

---

## 🔧 部署步骤

### 第 1 步：配置 DNS（5 分钟）
- [ ] 登录阿里云域名控制台
- [ ] 找到 cn2g.com 域名
- [ ] 添加 A 记录：@ → 119.28.137.229
- [ ] 添加 A 记录：www → 119.28.137.229
- [ ] 等待 DNS 生效（5-30 分钟）
- [ ] 验证 DNS：`nslookup cn2g.com`

### 第 2 步：连接服务器（2 分钟）
- [ ] 打开终端/命令行
- [ ] 连接到服务器：`ssh root@119.28.137.229`
- [ ] 输入密码或使用 SSH 密钥

### 第 3 步：上传文件（5 分钟）
- [ ] 创建应用目录：`mkdir -p /var/www/cn2global`
- [ ] 上传文件：`scp -r ./cn2global/* root@119.28.137.229:/var/www/cn2global/`
- [ ] 验证文件：`ls -la /var/www/cn2global/`

### 第 4 步：运行部署脚本（10-15 分钟）
- [ ] 给脚本执行权限：`chmod +x deploy.sh`
- [ ] 运行脚本：`sudo bash deploy.sh`
- [ ] 脚本会自动：
  - [ ] 更新系统
  - [ ] 安装 Node.js 18
  - [ ] 安装 MySQL
  - [ ] 安装 Nginx
  - [ ] 安装 PM2
  - [ ] 配置 Nginx
  - [ ] 申请 SSL 证书
  - [ ] 启动应用

### 第 5 步：配置 Google OAuth（5 分钟）
- [ ] 获取 Google OAuth 凭证
- [ ] 编辑 .env 文件：`nano /var/www/cn2global/api/.env`
- [ ] 填入 GOOGLE_CLIENT_ID
- [ ] 填入 GOOGLE_CLIENT_SECRET
- [ ] 填入 GOOGLE_REDIRECT_URI: `https://cn2g.com/api/auth/google/callback`
- [ ] 保存文件（Ctrl+O, Enter, Ctrl+X）

### 第 6 步：重启应用（2 分钟）
- [ ] 重启应用：`pm2 restart cn2global-api`
- [ ] 查看状态：`pm2 status`
- [ ] 查看日志：`pm2 logs cn2global-api`

---

## ✅ 验证部署

### 1. DNS 验证
```bash
# 在本地电脑运行
nslookup cn2g.com

# 应该看到：
# Name: cn2g.com
# Address: 119.28.137.229
```
- [ ] DNS 解析正确

### 2. 网站访问
- [ ] 访问 https://cn2g.com
- [ ] 页面正常加载
- [ ] 没有 SSL 证书错误

### 3. 功能测试
- [ ] 访问注册页面：https://cn2g.com/register_i18n.html
- [ ] 访问登录页面：https://cn2g.com/login_i18n.html
- [ ] 语言切换正常
- [ ] Google OAuth 按钮可见

### 4. API 测试
```bash
# 测试注册 API
curl -X POST https://cn2g.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"country":"CN","phone":"+8613800000000","password":"Test123456"}'

# 应该返回成功响应
```
- [ ] API 响应正常

### 5. 服务器状态
```bash
# 检查应用状态
pm2 status

# 应该看到 cn2global-api 处于 online 状态
```
- [ ] 应用运行正常
- [ ] MySQL 运行正常
- [ ] Nginx 运行正常

---

## 🔐 安全检查

- [ ] SSL 证书已安装
- [ ] HTTPS 强制重定向已配置
- [ ] 防火墙已配置
- [ ] .env 文件权限已限制：`chmod 600 .env`
- [ ] 数据库密码已更改
- [ ] JWT_SECRET 已更改

---

## 📊 性能检查

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

- [ ] 磁盘空间充足（> 1 GB）
- [ ] 内存使用正常（< 80%）
- [ ] CPU 使用正常（< 80%）
- [ ] Node.js 进程运行正常

---

## 📝 部署日志

### 部署时间
- 开始时间：_______________
- 结束时间：_______________
- 总耗时：_______________

### 部署人员
- 姓名：_______________
- 联系方式：_______________

### 备注
```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

---

## 🚨 常见问题

### Q: DNS 未生效怎么办？
A: 等待 5-30 分钟，DNS 需要时间传播。可以使用 `nslookup` 或 `dig` 命令验证。

### Q: SSL 证书申请失败怎么办？
A: 确保 DNS 已正确配置，Nginx 已启动，防火墙已开放 80 和 443 端口。

### Q: 应用无法启动怎么办？
A: 检查 .env 文件配置，查看 `pm2 logs cn2global-api` 日志，检查 MySQL 是否运行。

### Q: 如何查看实时日志？
A: 使用 `pm2 logs cn2global-api` 查看应用日志，使用 `tail -f /var/log/nginx/cn2global_access.log` 查看 Nginx 日志。

### Q: 如何重启应用？
A: 使用 `pm2 restart cn2global-api` 重启应用。

---

## 📞 技术支持

如有问题，请：
1. 查看服务器日志
2. 检查 DNS 配置
3. 验证 SSL 证书
4. 检查应用状态
5. 查看 .env 文件配置

---

## ✨ 部署完成

- [ ] 所有步骤已完成
- [ ] 所有验证已通过
- [ ] 网站已上线
- [ ] 用户可以访问 https://cn2g.com

**部署状态：✅ 完成**

---

**最后更新：2026-03-31**
