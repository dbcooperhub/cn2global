#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CN2Global 自动化部署脚本
连接到腾讯云服务器并完成完整部署
"""

import os
import sys
import paramiko
import time
from pathlib import Path

# 配置
SERVER_IP = "119.28.137.229"
SERVER_USER = "root"
SERVER_PASSWORD = "asdfg1988."
SSH_KEY_PATH = os.path.expanduser("~/Desktop/cn2g.pem")
REMOTE_PATH = "/var/www/cn2global"
LOCAL_PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# 颜色定义
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def connect_ssh():
    """连接到 SSH 服务器"""
    print_info("正在连接到服务器...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 尝试使用 SSH 密钥连接
        if os.path.exists(SSH_KEY_PATH):
            print_info(f"使用 SSH 密钥: {SSH_KEY_PATH}")
            ssh.connect(SERVER_IP, username=SERVER_USER, key_filename=SSH_KEY_PATH, timeout=10)
        else:
            # 使用密码连接
            print_info("使用密码连接")
            ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASSWORD, timeout=10)
        
        print_success("SSH 连接成功")
        return ssh
    except Exception as e:
        print_error(f"SSH 连接失败: {e}")
        sys.exit(1)

def execute_command(ssh, command, description=""):
    """执行远程命令"""
    if description:
        print_info(description)
    
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error and "warning" not in error.lower():
            print_warning(f"命令输出: {error}")
        
        return output
    except Exception as e:
        print_error(f"命令执行失败: {e}")
        return None

def upload_files(ssh, sftp):
    """上传项目文件到服务器"""
    print_info("第 1 步：上传项目文件")
    
    # 创建远程目录
    try:
        sftp.stat(REMOTE_PATH)
    except IOError:
        sftp.mkdir(REMOTE_PATH)
    
    # 上传文件
    files_to_upload = [
        'i18n.js',
        'register_i18n.html',
        'login_i18n.html',
        'index.html',
        'style.css',
        'deploy_complete.sh'
    ]
    
    for file in files_to_upload:
        local_file = os.path.join(LOCAL_PROJECT_PATH, file)
        remote_file = f"{REMOTE_PATH}/{file}"
        
        if os.path.exists(local_file):
            try:
                sftp.put(local_file, remote_file)
                print_success(f"已上传: {file}")
            except Exception as e:
                print_warning(f"上传失败 {file}: {e}")
    
    # 上传 api 目录
    api_files = ['server_i18n.js', 'package.json']
    for file in api_files:
        local_file = os.path.join(LOCAL_PROJECT_PATH, 'api', file)
        remote_file = f"{REMOTE_PATH}/api/{file}"
        
        if os.path.exists(local_file):
            try:
                sftp.put(local_file, remote_file)
                print_success(f"已上传: api/{file}")
            except Exception as e:
                print_warning(f"上传失败 api/{file}: {e}")

def deploy(ssh):
    """执行部署"""
    print_info("第 2 步：执行部署脚本")
    
    # 给脚本执行权限
    execute_command(ssh, f"chmod +x {REMOTE_PATH}/deploy_complete.sh", "设置脚本权限")
    
    # 执行部署脚本
    print_info("运行部署脚本（这可能需要 10-15 分钟）...")
    
    # 使用 sudo 执行脚本
    command = f"cd {REMOTE_PATH} && sudo bash deploy_complete.sh"
    stdin, stdout, stderr = ssh.exec_command(command)
    
    # 实时输出日志
    while True:
        line = stdout.readline().decode('utf-8')
        if not line:
            break
        print(line.rstrip())
    
    print_success("部署脚本执行完成")

def verify_deployment(ssh):
    """验证部署"""
    print_info("第 3 步：验证部署")
    
    # 检查应用状态
    output = execute_command(ssh, "pm2 status", "检查应用状态")
    if output and "cn2global-api" in output:
        print_success("应用已启动")
    else:
        print_warning("应用状态未知")
    
    # 检查 Nginx 状态
    output = execute_command(ssh, "systemctl status nginx", "检查 Nginx 状态")
    if output and "active (running)" in output:
        print_success("Nginx 已启动")
    else:
        print_warning("Nginx 状态未知")
    
    # 检查 MySQL 状态
    output = execute_command(ssh, "systemctl status mysql", "检查 MySQL 状态")
    if output and "active (running)" in output:
        print_success("MySQL 已启动")
    else:
        print_warning("MySQL 状态未知")

def main():
    """主函数"""
    print("")
    print("🚀 CN2Global 自动化部署脚本")
    print("=" * 50)
    print("")
    print(f"服务器 IP: {SERVER_IP}")
    print(f"用户名: {SERVER_USER}")
    print(f"项目路径: {LOCAL_PROJECT_PATH}")
    print("")
    
    # 连接 SSH
    ssh = connect_ssh()
    
    try:
        # 创建 SFTP 连接
        sftp = ssh.open_sftp()
        
        # 上传文件
        upload_files(ssh, sftp)
        
        # 关闭 SFTP
        sftp.close()
        
        # 执行部署
        deploy(ssh)
        
        # 验证部署
        verify_deployment(ssh)
        
        print("")
        print_success("部署完成！")
        print("")
        print("📍 访问地址:")
        print("  - 主页: https://cn2g.com")
        print("  - 注册: https://cn2g.com/register_i18n.html")
        print("  - 登录: https://cn2g.com/login_i18n.html")
        print("")
        print("📝 后续步骤:")
        print("  1. 编辑 /var/www/cn2global/api/.env，添加 Google OAuth 凭证")
        print("  2. 重启应用: pm2 restart cn2global-api")
        print("  3. 查看日志: pm2 logs cn2global-api")
        print("")
        
    except Exception as e:
        print_error(f"部署失败: {e}")
        sys.exit(1)
    finally:
        ssh.close()

if __name__ == "__main__":
    main()
