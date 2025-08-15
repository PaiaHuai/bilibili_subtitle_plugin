# B站字幕插件测试指南

本文档提供了如何测试和使用B站字幕提取插件的详细说明。

## 前提条件

在开始测试之前，请确保您已经：

1. 安装了所有必要的依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 拥有有效的B站账号和Cookie信息（SESSDATA, BILI_JCT, BUVID3）

## 获取B站Cookie信息

要使用此插件，您需要提供B站的Cookie信息。以下是获取这些信息的步骤：

1. 使用Chrome或Firefox浏览器登录B站官网 (https://www.bilibili.com/)
2. 登录成功后，按F12打开开发者工具
3. 切换到「Application」(Chrome) 或「Storage」(Firefox) 标签
4. 在左侧找到「Cookies」，然后选择「https://www.bilibili.com」
5. 在右侧的Cookie列表中找到并复制以下三个值：
   - SESSDATA
   - bili_jct
   - BUVID3

## 验证Cookie有效性

在使用插件之前，建议先验证您的Cookie是否有效：

1. 运行验证工具：
   ```bash
   python working/verify_credentials.py
   ```

2. 按照提示输入您的Cookie信息
3. 工具会告诉您Cookie是否有效

## 本地测试插件

### 方法1：使用测试脚本

我们提供了一个独立的测试脚本，可以直接测试插件的核心功能：

1. 创建一个`.env`文件，添加您的Cookie信息：
   ```
   SESSDATA=your_sessdata_here
   BILI_JCT=your_bili_jct_here
   BUVID3=your_buvid3_here
   ```

2. 运行测试脚本：
   ```bash
   python working/test_plugin.py
   ```

3. 脚本会使用默认的测试视频URL获取字幕，并显示结果

### 方法2：使用Dify本地开发服务器

如果您想在Dify环境中测试插件：

1. 确保您已安装Dify CLI工具

2. 启动本地开发服务器：
   ```bash
   python -m main
   ```

3. 服务器启动后，您可以通过Dify平台的「插件开发」功能进行测试

## 测试不同类型的视频

为了全面测试插件功能，建议使用不同类型的B站视频进行测试：

1. **带有官方字幕的视频**：
   - 例如：https://www.bilibili.com/video/BV1GJ411x7h7
   - 这类视频通常有B站官方提供的字幕

2. **带有UP主自制字幕的视频**：
   - 这类视频的字幕由UP主自己添加

3. **不同格式的视频URL**：
   - BV号格式：https://www.bilibili.com/video/BV1GJ411x7h7
   - av号格式：https://www.bilibili.com/video/av170001
   - 短链接：https://b23.tv/xxxxxx

## 常见问题排查

### 1. 无法获取字幕

可能的原因：
- 视频没有字幕
- Cookie已过期
- 网络连接问题

解决方案：
- 确认视频确实有字幕（在B站播放器中查看）
- 重新获取并验证Cookie
- 检查网络连接

### 2. Cookie验证失败

可能的原因：
- Cookie输入错误
- Cookie已过期
- B站服务器暂时无法访问

解决方案：
- 仔细检查Cookie信息，确保没有多余的空格
- 重新登录B站获取新的Cookie
- 稍后再试

### 3. 运行测试脚本时出错

可能的原因：
- 依赖库未正确安装
- Python版本不兼容
- 环境变量未正确设置

解决方案：
- 重新安装依赖：`pip install -r requirements.txt`
- 确保使用Python 3.8或更高版本
- 检查`.env`文件格式是否正确

## 提交反馈

如果您在测试过程中遇到任何问题，或有改进建议，请提交issue或联系插件作者。

---

祝您测试顺利！