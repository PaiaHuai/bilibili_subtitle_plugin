#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
B站凭证验证工具

此脚本用于验证B站Cookie信息(SESSDATA, BILI_JCT, BUVID3)是否有效。
使用方法：
1. 确保已安装所有依赖（pip install -r requirements.txt）
2. 在命令行中运行此脚本：python verify_credentials.py
3. 按照提示输入Cookie信息
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入凭证验证类
from provider.bilibili_subtitle_plugin import BilibiliSubtitlePluginProvider


async def main():
    print("===== B站凭证验证工具 =====")
    print("此工具用于验证B站Cookie信息是否有效")
    print("\n请提供以下信息：\n")
    
    # 获取用户输入
    sessdata = input("请输入SESSDATA: ")
    bili_jct = input("请输入BILI_JCT: ")
    buvid3 = input("请输入BUVID3: ")
    
    # 创建凭证字典
    credentials = {
        "sessdata": sessdata,
        "bili_jct": bili_jct,
        "buvid3": buvid3
    }
    
    # 创建提供者实例
    provider = BilibiliSubtitlePluginProvider()
    
    try:
        # 验证凭证
        print("\n正在验证凭证，请稍候...\n")
        await provider._validate_credentials(credentials)
        print("✅ 凭证验证成功！这些Cookie信息可以用于B站字幕提取插件。")
    except Exception as e:
        print(f"❌ 凭证验证失败: {str(e)}")
        print("请检查您的Cookie信息是否正确，或者Cookie可能已经过期。")
    
    print("\n===== 验证完成 =====")


if __name__ == "__main__":
    asyncio.run(main())