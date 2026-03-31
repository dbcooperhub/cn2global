# CN2Global 国际化完整部署指南

## 📋 项目概述

这是 CN2Global 网站的完整国际化和认证系统重构，包括：
- ✅ 多语言支持（中文、英文、日文、德文、法文）
- ✅ 手机号注册（带国家区号自动匹配）
- ✅ Google OAuth 第三方登录
- ✅ 国际化客服系统
- ✅ 完整的后端 API

## 🚀 快速开始

### 1. 环境配置

#### 创建 `.env` 文件

```bash
# 数据库配置
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=Asd1988.
DB_NAME=cn2global

# JWT 配置
JWT_SECRET=your-secret-key-here-change-in-production

# Google OAuth 配置
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/api/auth/google/callback

# 服务器配置
PORT=3000
NODE_ENV=development
```

### 2. 获取 Google OAuth 凭证

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目
3. 启用 Google+ API
4. 创建 OAuth 2.0 凭证（Web 应用）
5. 添加授权重定向 URI：
   - 本地开发：`http://localhost:3000/api/auth/google/callback`
   - 生产环境：`https://cn2g.com/api/auth/google/callback`
6. 复制 Client ID 和 Client Secret 到 `.env` 文件

### 3. 安装依赖

```bash
cd api
npm install
```

### 4. 启动服务器

```bash
# 开发环境
npm start

# 或使用 nodemon（自动重启）
npx nodemon server_i18n.js
```

## 📁 文件结构

```
cn2global/
├── i18n.js                    # 国际化配置和翻译
├── register_i18n.html         # 国际化注册页面
├── login_i18n.html            # 国际化登录页面
├── index.html                 # 主页（需要更新）
├── api/
│   ├── server_i18n.js         # 国际化后端 API
│   ├── .env                   # 环境变量
│   └── package.json
└── public/                    # 静态文件
```

## 🔧 核心功能

### 1. 国际化系统 (i18n.js)

**支持的语言：**
- 中文 (zh)
- 英文 (en)
- 日文 (ja)
- 德文 (de)
- 法文 (fr)

**国家和区号映射：**
- 中国 (+86)
- 美国 (+1)
- 英国 (+44)
- 日本 (+81)
- 德国 (+49)
- 法国 (+33)
- 加拿大 (+1)
- 澳大利亚 (+61)
- 新加坡 (+65)
- 香港 (+852)
- 台湾 (+886)
- 韩国 (+82)
- 印度 (+91)
- 巴西 (+55)
- 墨西哥 (+52)
- 新西兰 (+64)
- 泰国 (+66)
- 马来西亚 (+60)
- 菲律宾 (+63)
- 越南 (+84)

**使用方法：**

```javascript
// 获取翻译
const text = t('register.title', 'en');  // "Create Account"

// 设置语言
setLanguage('zh');  // 切换到中文

// 获取用户语言
const lang = getUserLanguage();  // 自动检测浏览器语言
```

### 2. 注册流程 (register_i18n.html)

**功能：**
- 国家/地区选择（自动匹配区号）
- 手机号验证
- 邮箱验证（可选）
- 密码强度检查
- 条款同意
- Google OAuth 集成

**API 端点：**
```
POST /api/auth/register
Content-Type: application/json

{
  "country": "CN",
  "phone": "+8613800000000",
  "email": "user@example.com",
  "password": "SecurePassword123",
  "language": "zh"
}

Response:
{
  "message": "Registration successful",
  "redirect": "/login_i18n.html"
}
```

### 3. 登录流程 (login_i18n.html)

**功能：**
- 手机号 + 密码登录
- Google OAuth 登录
- 记住登录状态
- 忘记密码链接

**API 端点：**
```
POST /api/auth/login
Content-Type: application/json

{
  "phone": "+8613800000000",
  "password": "SecurePassword123",
  "language": "zh"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "phone": "+8613800000000",
    "email": "user@example.com",
    "name": "User Name",
    "country": "CN",
    "language": "zh",
    "member_level": "normal"
  }
}
```

### 4. Google OAuth 流程

**步骤：**
1. 用户点击 "Sign in with Google"
2. 重定向到 `/api/auth/google`
3. Google 授权页面
4. 回调到 `/api/auth/google/callback`
5. 自动创建或登录用户
6. 重定向到仪表板

### 5. 客服系统 (API)

**获取客服信息：**
```
GET /api/support/info?lang=zh

Response:
{
  "title": "客户支持",
  "channels": [
    {
      "type": "chat",
      "name": "在线客服",
      "available": true,
      "hours": "9:00-18:00"
    },
    ...
  ]
}
```

**提交客服工单：**
```
POST /api/support/ticket
Authorization: Bearer <token>
Content-Type: application/json

{
  "subject": "问题标题",
  "message": "问题描述",
  "category": "shipping"
}

Response:
{
  "message": "Ticket created successfully",
  "ticket_number": "TK-1234567890"
}
```

## 🗄️ 数据库架构

### Users 表
```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  phone VARCHAR(20) UNIQUE,
  email VARCHAR(100) UNIQUE,
  password VARCHAR(255),
  name VARCHAR(100),
  country VARCHAR(10),
  language VARCHAR(10) DEFAULT 'en',
  google_id VARCHAR(255) UNIQUE,
  member_level ENUM('normal', 'silver', 'gold', 'diamond'),
  points INT DEFAULT 0,
  balance DECIMAL(10,2) DEFAULT 0.00,
  phone_verified BOOLEAN DEFAULT FALSE,
  email_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Verification Codes 表
```sql
CREATE TABLE verification_codes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  phone VARCHAR(20) NOT NULL,
  code VARCHAR(6) NOT NULL,
  attempts INT DEFAULT 0,
  expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔐 安全最佳实践

1. **密码加密**
   - 使用 bcryptjs 加密密码
   - 最小 8 个字符
   - 包含大小写字母和数字

2. **JWT Token**
   - 有效期 7 天
   - 存储在 localStorage
   - 每个请求都验证

3. **CORS 配置**
   - 允许跨域请求
   - 生产环境限制来源

4. **输入验证**
   - 使用 express-validator
   - 验证所有用户输入
   - 防止 SQL 注入

5. **HTTPS**
   - 生产环境必须使用 HTTPS
   - 更新 Google OAuth 重定向 URI

## 📱 前端集成

### 在主页中添加语言切换

```html
<!-- 在导航栏中添加 -->
<div class="lang-selector">
  <button class="lang-btn" data-lang="en">English</button>
  <button class="lang-btn" data-lang="zh">中文</button>
  <button class="lang-btn" data-lang="ja">日本語</button>
  <button class="lang-btn" data-lang="de">Deutsch</button>
  <button class="lang-btn" data-lang="fr">Français</button>
</div>

<script src="i18n.js"></script>
<script>
  // 初始化语言
  let currentLang = getUserLanguage();
  setLanguage(currentLang);

  // 语言切换
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.getAttribute('data-lang');
      setLanguage(lang);
    });
  });
</script>
```

### 使用翻译

```html
<!-- 在 HTML 中使用 data-i18n 属性 -->
<h1 data-i18n="hero.title">Ship from Qingdao to the World</h1>
<p data-i18n="hero.subtitle">...</p>

<!-- 在 JavaScript 中使用 -->
<script>
  const title = t('hero.title', 'en');
  console.log(title);  // "Ship from Qingdao to the World"
</script>
```

## 🚢 部署指南

### 1. 本地开发

```bash
# 启动 MySQL
# 启动 Node.js 服务器
npm start

# 访问
http://localhost:3000
```

### 2. 生产部署（使用 PM2）

```bash
# 安装 PM2
npm install -g pm2

# 启动应用
pm2 start api/server_i18n.js --name "cn2global"

# 设置开机自启
pm2 startup
pm2 save

# 查看日志
pm2 logs cn2global
```

### 3. Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name cn2g.com www.cn2g.com;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cn2g.com www.cn2g.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # 静态文件
    location / {
        root /var/www/cn2global;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 4. Docker 部署

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "api/server_i18n.js"]
```

```bash
# 构建镜像
docker build -t cn2global:latest .

# 运行容器
docker run -d \
  --name cn2global \
  -p 3000:3000 \
  -e DB_HOST=mysql \
  -e GOOGLE_CLIENT_ID=xxx \
  -e GOOGLE_CLIENT_SECRET=xxx \
  cn2global:latest
```

## 🧪 测试

### 注册测试

```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "country": "CN",
    "phone": "+8613800000000",
    "email": "test@example.com",
    "password": "TestPassword123",
    "language": "zh"
  }'
```

### 登录测试

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+8613800000000",
    "password": "TestPassword123",
    "language": "zh"
  }'
```

### 获取用户信息

```bash
curl -X GET http://localhost:3000/api/user/profile \
  -H "Authorization: Bearer <token>"
```

## 📊 监控和日志

### 启用日志

```javascript
// 在 server_i18n.js 中添加
const morgan = require('morgan');
app.use(morgan('combined'));
```

### 错误追踪

```javascript
// 使用 Sentry 进行错误追踪
const Sentry = require("@sentry/node");
Sentry.init({ dsn: "your-sentry-dsn" });
app.use(Sentry.Handlers.errorHandler());
```

## 🔄 更新和维护

### 添加新语言

1. 在 `i18n.js` 中添加翻译
2. 在 `countryData` 中添加国家
3. 在前端语言选择器中添加按钮

### 添加新国家

```javascript
// 在 i18n.js 中
countryData['IT'] = { name: 'Italia', code: '+39', lang: 'en' };
```

## 📞 支持

如有问题，请联系：
- 邮件：support@cn2global.com
- 电话：+86-532-8888-8888
- 在线客服：https://cn2g.com

---

**最后更新：2026-03-31**
**版本：1.0.0**
