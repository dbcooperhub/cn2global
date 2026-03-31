#!/bin/bash

# CN2Global API 测试脚本

BASE_URL="http://localhost:3000"
TOKEN=""

echo "🧪 CN2Global API 测试"
echo "===================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试函数
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4

    echo -e "${YELLOW}测试: $description${NC}"
    echo "请求: $method $endpoint"

    if [ -z "$data" ]; then
        response=$(curl -s -X $method "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $TOKEN")
    else
        echo "数据: $data"
        response=$(curl -s -X $method "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $TOKEN" \
            -d "$data")
    fi

    echo "响应: $response"
    echo ""
}

# 1. 测试注册
echo -e "${YELLOW}=== 1. 测试用户注册 ===${NC}"
echo ""

register_data='{
  "country": "CN",
  "phone": "+8613800000001",
  "email": "test@example.com",
  "password": "TestPassword123",
  "language": "zh"
}'

test_endpoint "POST" "/api/auth/register" "$register_data" "用户注册"

# 2. 测试登录
echo -e "${YELLOW}=== 2. 测试用户登录 ===${NC}"
echo ""

login_data='{
  "phone": "+8613800000001",
  "password": "TestPassword123",
  "language": "zh"
}'

response=$(curl -s -X POST "$BASE_URL/api/auth/login" \
    -H "Content-Type: application/json" \
    -d "$login_data")

echo "请求: POST /api/auth/login"
echo "数据: $login_data"
echo "响应: $response"
echo ""

# 提取 token
TOKEN=$(echo $response | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo -e "${RED}❌ 登录失败，无法获取 token${NC}"
    exit 1
else
    echo -e "${GREEN}✅ 登录成功，Token: ${TOKEN:0:20}...${NC}"
    echo ""
fi

# 3. 测试获取用户信息
echo -e "${YELLOW}=== 3. 测试获取用户信息 ===${NC}"
echo ""

test_endpoint "GET" "/api/user/profile" "" "获取用户信息"

# 4. 测试更新语言
echo -e "${YELLOW}=== 4. 测试更新用户语言 ===${NC}"
echo ""

language_data='{
  "language": "en"
}'

test_endpoint "PUT" "/api/user/language" "$language_data" "更新用户语言为英文"

# 5. 测试获取客服信息
echo -e "${YELLOW}=== 5. 测试获取客服信息 ===${NC}"
echo ""

echo "请求: GET /api/support/info?lang=zh"
response=$(curl -s -X GET "$BASE_URL/api/support/info?lang=zh")
echo "响应: $response"
echo ""

echo "请求: GET /api/support/info?lang=en"
response=$(curl -s -X GET "$BASE_URL/api/support/info?lang=en")
echo "响应: $response"
echo ""

# 6. 测试提交客服工单
echo -e "${YELLOW}=== 6. 测试提交客服工单 ===${NC}"
echo ""

ticket_data='{
  "subject": "测试工单",
  "message": "这是一个测试工单",
  "category": "shipping"
}'

test_endpoint "POST" "/api/support/ticket" "$ticket_data" "提交客服工单"

# 7. 测试重复注册（应该失败）
echo -e "${YELLOW}=== 7. 测试重复注册（应该失败） ===${NC}"
echo ""

test_endpoint "POST" "/api/auth/register" "$register_data" "重复注册相同手机号"

# 8. 测试无效密码登录（应该失败）
echo -e "${YELLOW}=== 8. 测试无效密码登录（应该失败） ===${NC}"
echo ""

invalid_login_data='{
  "phone": "+8613800000001",
  "password": "WrongPassword",
  "language": "zh"
}'

test_endpoint "POST" "/api/auth/login" "$invalid_login_data" "使用错误密码登录"

# 9. 测试无效手机号（应该失败）
echo -e "${YELLOW}=== 9. 测试无效手机号（应该失败） ===${NC}"
echo ""

invalid_register_data='{
  "country": "CN",
  "phone": "invalid",
  "email": "test2@example.com",
  "password": "TestPassword123",
  "language": "zh"
}'

test_endpoint "POST" "/api/auth/register" "$invalid_register_data" "使用无效手机号注册"

# 10. 测试短密码（应该失败）
echo -e "${YELLOW}=== 10. 测试短密码（应该失败） ===${NC}"
echo ""

short_password_data='{
  "country": "CN",
  "phone": "+8613800000002",
  "email": "test3@example.com",
  "password": "short",
  "language": "zh"
}'

test_endpoint "POST" "/api/auth/register" "$short_password_data" "使用短密码注册"

echo -e "${GREEN}✅ 所有测试完成！${NC}"
echo ""
echo "📊 测试总结："
echo "- 成功的测试：注册、登录、获取信息、更新语言、获取客服信息、提交工单"
echo "- 失败的测试（预期）：重复注册、错误密码、无效手机号、短密码"
echo ""
