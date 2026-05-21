#!/usr/bin/env python3
"""
抖音 Cookie 配置工具
用于设置抖音 API 访问所需的认证信息
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.douyin_config import DouyinConfig

def print_banner():
    print("=" * 60)
    print("  抖音商品采集工具 - Cookie 配置向导")
    print("=" * 60)
    print()

def print_instructions():
    print("【Cookie 获取步骤】")
    print("1. 使用 Chrome/Edge 浏览器访问 https://www.douyin.com/")
    print("2. 登录您的抖音账号（已登录可跳过）")
    print("3. 按 F12 打开开发者工具")
    print("4. 切换到 'Network'（网络）选项卡")
    print("5. 勾选 'Preserve log'（保留日志）")
    print("6. 在 Filter（筛选器）输入框中输入：cookie")
    print("7. 在页面上点击任意视频或刷新页面")
    print("8. 点击任意一个网络请求")
    print("9. 在右侧找到 'Request Headers' 或 'Headers'")
    print("10. 找到 'cookie:' 字段，复制其全部内容")
    print()
    print("【Device ID 获取步骤】")
    print("1. 在开发者工具的网络请求中搜索：device_id")
    print("2. 找到包含 device_id 的请求")
    print("3. 复制 device_id 的值")
    print()
    print("⚠️  注意：Cookie 非常敏感，请勿泄露给他人！")
    print()

def get_cookie_input():
    print("请粘贴您的抖音 Cookie（包含odin_tt字段）：")
    print("(直接按回车跳过，稍后可再次配置)")
    cookie = input("> ").strip()
    return cookie

def get_device_id_input():
    print()
    print("请粘贴您的 Device ID（可选）：")
    print("(直接按回车跳过)")
    device_id = input("> ").strip()
    return device_id

def main():
    print_banner()
    print_instructions()
    
    config = DouyinConfig()
    
    if config.is_configured():
        print("✓ 您已经配置了有效的 Cookie")
        print()
        response = input("是否要更新 Cookie？(y/N): ").strip().lower()
        if response != 'y':
            print("配置保持不变，退出程序。")
            return
    
    cookie = get_cookie_input()
    
    if not cookie:
        print("未输入 Cookie，退出程序。")
        print("您可以稍后再次运行此程序进行配置。")
        return
    
    device_id = get_device_id_input()
    
    if 'odin_tt' not in cookie:
        print()
        print("⚠️  警告：Cookie 中未找到 'odin_tt' 字段！")
        print("这可能导致 API 请求失败。")
        print()
        confirm = input("是否继续保存？(y/N): ").strip().lower()
        if confirm != 'y':
            print("取消保存，退出程序。")
            return
    
    config.save(cookie=cookie, device_id=device_id)
    
    print()
    print("=" * 60)
    print("✓ Cookie 配置成功！")
    print("=" * 60)
    print()
    print("您现在可以运行程序进行商品数据采集：")
    print("  - Web 模式: python app.py")
    print("  - 命令行模式: python cli.py -k \"关键词\"")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已退出。")
    except Exception as e:
        print(f"\n发生错误: {e}")
        input("\n按回车键退出...")
