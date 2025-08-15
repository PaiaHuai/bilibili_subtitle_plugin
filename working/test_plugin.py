#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
B站字幕插件测试脚本

此脚本用于测试B站字幕插件的功能，直接调用插件的工具类进行测试。
使用方法：
1. 确保已安装所有依赖（pip install -r requirements.txt）
2. 在命令行中运行此脚本：python test_plugin.py
"""

import asyncio
import sys
import os
import json
from typing import Any, Dict

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入插件工具类
from tools.bilibili_subtitle_plugin import BilibiliSubtitlePluginTool

# 测试用的凭证信息 - 从环境变量或.env文件中获取
from dotenv import load_dotenv
load_dotenv()

SESS_DATA = os.getenv("SESSDATA", "")
BILI_JCT = os.getenv("BILI_JCT", "")
BUVID3 = os.getenv("BUVID3", "")

# 测试用的视频ID列表
TEST_VIDEOS = [
    {"id": "BV1sthHzaEcH", "type": "BV号视频"},
    {"id": "av170001", "type": "av号视频"},
    {"id": "170001", "type": "纯数字（自动转换为av号）"}
]

# 默认测试视频
DEFAULT_TEST_VIDEO = TEST_VIDEOS[0]["id"]

# 模拟运行时环境
class MockRuntime:
    def __init__(self, credentials):
        self.credentials = credentials

class MockSession:
    def __init__(self):
        pass

# 收集工具输出的函数
def collect_tool_output(tool, video_id):
    results = []
    for message in tool._invoke({"video_id": video_id}):
        results.append(message)
    return results

# 主函数
def main():
    print("===== B站字幕插件测试 =====\n")
    
    # 检查凭证
    if not SESS_DATA or not BILI_JCT or not BUVID3:
        print("错误：缺少必要的凭证信息。请在.env文件中设置SESSDATA, BILI_JCT和BUVID3。")
        return
    
    # 创建模拟运行时环境
    runtime = MockRuntime({
        "sessdata": SESS_DATA,
        "bili_jct": BILI_JCT,
        "buvid3": BUVID3
    })
    session = MockSession()
    
    # 创建工具实例
    tool = BilibiliSubtitlePluginTool(runtime=runtime, session=session)
    
    # 询问用户选择测试模式
    print("请选择测试模式：")
    print("1. 测试单个视频 (默认)")
    print("2. 测试所有支持的视频格式")
    choice = input("请输入选项 (1/2): ").strip() or "1"
    
    if choice == "1":
        # 测试单个视频
        test_single_video(tool)
    else:
        # 测试所有视频格式
        test_all_video_formats(tool)
    
    print("\n===== 测试完成 =====")

# 测试单个视频
def test_single_video(tool):
    # 询问用户输入视频ID或使用默认值
    video_id = input(f"请输入B站视频ID (BV号/av号/纯数字，直接回车使用默认视频): ").strip() or DEFAULT_TEST_VIDEO
    
    print(f"\n测试视频ID: {video_id}\n")
    
    # 执行工具并收集输出
    try:
        print("正在获取字幕...\n")
        results = collect_tool_output(tool, video_id)
        process_results(results)
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        import traceback
        print(traceback.format_exc())

# 测试所有视频格式
def test_all_video_formats(tool):
    for i, test_video in enumerate(TEST_VIDEOS):
        video_id = test_video["id"]
        video_type = test_video["type"]
        
        print(f"\n===== 测试 {video_type} =====")
        print(f"视频ID: {video_id}\n")
        
        try:
            print("正在获取字幕...")
            results = collect_tool_output(tool, video_id)
            process_results(results)
        except Exception as e:
            print(f"测试过程中发生错误: {str(e)}")
            print("继续测试下一个视频...")
        
        # 如果不是最后一个视频，添加分隔线
        if i < len(TEST_VIDEOS) - 1:
            print("\n" + "-" * 50)

# 处理并显示结果
def process_results(results):
    if results:
        print("获取字幕成功！\n")
        
        # 打印JSON结果
        for i, result in enumerate(results):
            print(f"结果 {i+1}:")
            if hasattr(result, 'json_object'):
                # JSON消息
                json_data = result.json_object
                print("\n----- 视频信息 -----")
                print(f"标题: {json_data.get('video_title', '未知标题')}")
                print(f"作者: {json_data.get('video_author', '未知作者')}")
                print(f"字幕语言: {json_data.get('subtitle_language', '未知')}")
                
                print("\n----- 字幕内容 -----")
                subtitles = json_data.get('subtitles', '')
                if subtitles:
                    # 只打印前10行字幕
                    subtitle_lines = subtitles.split('\n')[:10]
                    for line in subtitle_lines:
                        print(line)
                    if len(subtitle_lines) < len(subtitles.split('\n')):
                        print("... (更多字幕内容已省略)")
                else:
                    print("该视频没有可用的字幕")
            elif hasattr(result, 'text'):
                # 文本消息
                print(f"文本消息: {result.text}")
            else:
                # 其他类型消息
                print(f"未知类型消息: {result}")
            print()
    else:
        print("未获取到任何结果")

# 程序入口
if __name__ == "__main__":
    main()