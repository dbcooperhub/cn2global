# CN2Global 国际化 - 快速参考卡

## 🎯 项目完成情况

```
✅ 国际化系统        ✅ 注册页面         ✅ 登录页面
✅ 后端 API          ✅ 数据库架构       ✅ 完整文档
✅ 启动脚本          ✅ 测试脚本         ✅ 部署指南
```

## 📁 关键文件位置

```
cn2global/
├── i18n.js                    # 国际化配置
├── register_i18n.html         # 注册页面
├── login_i18n.html            # 登录页面
├── api/server_i18n.js         # API 服务器
├── DEPLOYMENT_GUIDE.md        # 部署指南
├── IMPLEMENTATION_CHECKLIST.md # 实现清单
├── DELIVERY_SUMMARY.md        # 交付总结
├── start.sh                   # Linux/Mac 启动
├── start.bat                  # Windows 启动
└── test_api.sh                # API 测试
```

## 🚀 3 步快速启动

### 1️⃣ 配置 Google OAuth
```
访问: https://console.cloud.google.com/
创建项目 → 启用 Google+ API → 创建 OAuth 凭证
复制 Client ID 和 Secret
```

### 2️⃣ 编辑环境变量
```bash
cd cn2global/api
nano .env  # 或用记事本打开
# 添加 Google OAuth 凭证和数据库配置
```

### 3️⃣ 启动服务器
```bash
# Windows
start.bat

# Linux/Mac
bash ../start.sh
```

**访问：** http://localhost:3000/register_i18n.html

## 🌍 支持的语言和国家

| 语言 | 国家 | 区号 |
|------|------|------|
| 中文 | 中国、香港、台湾 | +86, +852, +886 |
| 英文 | 美国、英国、加拿大、澳大利亚等 | +1, +44, +61 |
| 日文 | 日本、韩国 | +81, +82 |
| 德文 | 德国 | +49 |
| 法文 | 法国 | +33 |

## 📱 核心功能

### 注册流程
```
选择国家 → 输入手机号 → 输入密码 → 同意条款 → 注册
或
点击 Google 登录 → 授权 → 自动创建账户
```

### 登录流程
```
输入手机号 → 输入密码 → 登录
或
点击 Google 登录 → 授权 → 自动登录
```

### 语言切换
```
点击语言按钮 → 页面自动翻译 → 语言保存到 localStorage
```

## 🔧 API 端点

| 方法 | 端点 | 功能 |
|------|------|------|
| POST | /api/auth/register | 用户注册 |
| POST | /api/auth/login | 用户登录 |
| GET | /api/auth/google | Google OAuth |
| GET | /api/user/profile | 获取用户信息 |
| PUT | /api/user/language | 更新语言 |
| GET | /api/support/info | 获取客服信息 |
| POST | /api/support/ticket | 提交工单 |

## 🧪 测试

### 快速测试
```bash
bash test_api.sh
```

### 手动测试
```bash
# 注册
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"country":"CN","phone":"+8613800000000","password":"Test123456"}'

# 登录
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"+8613800000000","password":"Test123456"}'
```

## 📊 技术栈

```
前端：HTML5 + CSS3 + JavaScript (ES6+)
后端：Node.js + Express
数据库：MySQL 5.7+
认证：JWT + bcryptjs
验证：express-validator
OAuth：Google OAuth 2.0
```

## 🔐 安全特性

- ✅ 密码加密（bcryptjs）
- ✅ JWT Token 验证
- ✅ CORS 配置
- ✅ 输入验证
- ✅ SQL 注入防护
- ✅ XSS 防护

## 📖 文档

| 文件 | 内容 |
|------|------|
| DEPLOYMENT_GUIDE.md | 完整部署指南 |
| IMPLEMENTATION_CHECKLIST.md | 实现清单 |
| DELIVERY_SUMMARY.md | 交付总结 |

## ⚙️ 环境变量 (.env)

```env
# 数据库
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=cn2global

# JWT
JWT_SECRET=your-secret-key

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/api/auth/google/callback

# 服务器
PORT=3000
NODE_ENV=development
```

## 🎯 常见问题

### Q: 如何添加新语言？
A: 在 i18n.js 中添加翻译对象，然后在前端添加语言按钮

### Q: 如何添加新国家？
A: 在 i18n.js 的 countryData 中添加国家信息

### Q: 如何修改客服信息？
A: 编辑 server_i18n.js 中的 supportInfo 对象

### Q: 如何启用 HTTPS？
A: 配置 Nginx/Apache 反向代理，获取 SSL 证书

### Q: 如何部署到生产环境？
A: 参考 DEPLOYMENT_GUIDE.md 中的部署指南

## 📞 快速支持

| 问题 | 解决方案 |
|------|--------|
| 无法启动 | 检查 Node.js 版本、npm 依赖 |
| 数据库连接失败 | 检查 .env 配置、MySQL 是否运行 |
| Google OAuth 失败 | 检查 Client ID/Secret、重定向 URI |
| 页面不显示 | 检查浏览器控制台错误、清除缓存 |
| API 返回 500 | 检查服务器日志、数据库连接 |

## 🚀 部署检查清单

- [ ] 配置 Google OAuth 凭证
- [ ] 配置数据库连接
- [ ] 编辑 .env 文件
- [ ] 安装 npm 依赖
- [ ] 启动服务器
- [ ] 测试注册功能
- [ ] 测试登录功能
- [ ] 测试 Google OAuth
- [ ] 测试语言切换
- [ ] 测试客服功能

## 💡 性能优化建议

1. 启用数据库连接池
2. 使用 CDN 加速静态文件
3. 启用 Gzip 压缩
4. 添加缓存策略
5. 使用 PM2 进程管理

## 📈 监控指标

- 页面加载时间：< 2 秒
- API 响应时间：< 200 ms
- 数据库查询时间：< 50 ms
- 支持并发用户：1000+

## 🎁 额外资源

- [Express.js 文档](https://expressjs.com/)
- [JWT 介绍](https://jwt.io/)
- [Google OAuth 文档](https://developers.google.com/identity/protocols/oauth2)
- [MySQL 文档](https://dev.mysql.com/doc/)

---

**版本：1.0.0 | 状态：生产就绪 ✅**

**最后更新：2026-03-31**
