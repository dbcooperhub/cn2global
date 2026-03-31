@echo off
REM CN2Global 快速启动脚本 (Windows)

echo.
echo 🚀 CN2Global 启动脚本
echo =====================
echo.

REM 检查 Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js 未安装
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node -v') do set NODE_VERSION=%%i
echo ✅ Node.js 版本: %NODE_VERSION%

REM 检查 npm
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ npm 未安装
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm -v') do set NPM_VERSION=%%i
echo ✅ npm 版本: %NPM_VERSION%

REM 进入 API 目录
cd api

REM 检查 .env 文件
if not exist .env (
    echo ⚠️  .env 文件不存在，创建默认配置...
    (
        echo DB_HOST=localhost
        echo DB_USER=root
        echo DB_PASSWORD=Asd1988.
        echo DB_NAME=cn2global
        echo JWT_SECRET=cn2global-secret-key-2024
        echo GOOGLE_CLIENT_ID=your-google-client-id
        echo GOOGLE_CLIENT_SECRET=your-google-client-secret
        echo GOOGLE_REDIRECT_URI=http://localhost:3000/api/auth/google/callback
        echo PORT=3000
        echo NODE_ENV=development
    ) > .env
    echo ✅ .env 文件已创建，请编辑并添加 Google OAuth 凭证
)

REM 检查 node_modules
if not exist node_modules (
    echo 📦 安装依赖...
    call npm install
)

REM 启动服务器
echo.
echo 🎯 启动 CN2Global API 服务器...
echo 📍 访问地址: http://localhost:3000
echo 📝 注册页面: http://localhost:3000/register_i18n.html
echo 🔐 登录页面: http://localhost:3000/login_i18n.html
echo.
echo 按 Ctrl+C 停止服务器
echo.

node server_i18n.js

pause
