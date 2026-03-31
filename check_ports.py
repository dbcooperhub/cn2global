#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import time

def check_port(host, port, timeout=5):
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"错误: {e}")
        return False

def main():
    host = "119.28.137.229"
    ports = [22, 80, 443, 3000, 8080]
    
    print(f"🔍 检查服务器 {host} 的端口状态")
    print("=" * 50)
    
    for port in ports:
        status = "✅ 开放" if check_port(host, port) else "❌ 关闭"
        print(f"端口 {port:5d}: {status}")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
