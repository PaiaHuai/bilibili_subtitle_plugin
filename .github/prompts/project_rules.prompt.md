## 文件结构与组织原则

### 标准项目结构

```
your_plugin/
├── _assets/             # 图标和视觉资源
├── provider/            # 提供者定义和验证
│   ├── your_plugin.py   # 凭证验证逻辑
│   └── your_plugin.yaml # 提供者配置
├── tools/               # 工具实现
│   ├── feature_one.py   # 工具功能实现
│   ├── feature_one.yaml # 工具参数和描述
│   ├── feature_two.py   # 另一个工具实现
│   └── feature_two.yaml # 另一个工具配置
├── utils/               # 辅助函数
│   └── helpers.py       # 通用功能逻辑
├── working/             # 进度记录和工作文件
├── .env.example         # 环境变量模板
├── main.py              # 入口文件
├── manifest.yaml        # 插件主配置
├── README.md            # 文档
└── requirements.txt     # 依赖列表
```

### 文件组织核心原则

1. **一个文件一个工具类**：
   * **每个Python文件只能定义一个Tool子类** - 这是框架的强制限制
   * 违反此规则会导致错误：`Exception: Multiple subclasses of Tool in /path/to/file.py`
   * 示例：`tools/encrypt.py`只能包含`EncryptTool`类，不能同时包含`DecryptTool`

2. **命名和功能对应**：
   * Python文件名应与工具功能相对应
   * 工具类名应遵循`FeatureTool`的命名模式
   * YAML文件名应与对应的Python文件名保持一致

3. **文件位置指导**：
   * 通用工具函数放在`utils/`目录
   * 具体工具实现放在`tools/`目录
   * 凭证验证逻辑放在`provider/`目录

4. **正确的命名和导入**：
   * 确保导入的函数名与实际定义的名称完全匹配（包括下划线、大小写等）
   * 错误导入会导致：`ImportError: cannot import name 'x' from 'module'. Did you mean: 'y'?`

### 创建新工具的正确流程

1. **复制现有文件作为模板**：
   ```bash
   # 复制工具YAML文件作为模板
   cp tools/existing_tool.yaml tools/new_feature.yaml
   # 复制工具Python实现
   cp tools/existing_tool.py tools/new_feature.py
   ```

2. **编辑复制的文件**：
   * 更新YAML中的名称、描述和参数
   * 更新Python文件中的类名和实现逻辑
   * 确保每个文件只包含一个Tool子类

3. **更新provider配置**：
   * 在`provider/your_plugin.yaml`中添加新工具：
     ```yaml
     tools:
       - tools/existing_tool.yaml
       - tools/new_feature.yaml  # 添加新工具
     ```

### 常见错误排查

当遇到`Multiple subclasses of Tool`错误时：

1. **检查问题文件**：
   * 寻找形如`class AnotherTool(Tool):`的额外类定义
   * 确保文件中只有一个继承自`Tool`的类
   * 例如：如果`encrypt.py`包含`EncryptTool`和`DecryptTool`，保留`EncryptTool`并将`DecryptTool`移至`decrypt.py`

2. **检查导入错误**：
   * 确认导入的函数名或类名是否拼写正确
   * 注意下划线、大小写等细节
   * 修正导入语句中的拼写错误## 文件结构与代码组织规范

### 工具文件组织的严格限制

1. **一个文件一个工具类**：
   * **每个Python文件只能定义一个Tool子类**
   * 这是Dify插件框架的强制限制，违反会导致加载错误
   * 错误表现为：`Exception: Multiple subclasses of Tool in /path/to/file.py`

2. **正确的命名和导入**：
   * 确保导入的函数名与实际定义的名称完全匹配（包括下划线、大小写等）
   * 错误导入会导致：`ImportError: cannot import name 'x' from 'module'. Did you mean: 'y'?`

3. **创建新工具的正确流程**：
   * **步骤1**: 创建专门的YAML文件：`tools/new_feature.yaml`
   * **步骤2**: 创建对应的Python文件：`tools/new_feature.py`，确保一个文件只有一个Tool子类
   * **步骤3**: 更新provider YAML文件中的tools列表以包含新工具
   * **切勿**在现有工具文件中添加新工具类

### 代码错误排查指南

当遇到 `Multiple subclasses of Tool` 错误时：

1. **检查文件内容**：
   ```bash
   # 查看工具文件内容
   cat tools/problematic_file.py
   ```

2. **查找多余的Tool子类**：
   * 寻找形如 `class AnotherTool(Tool):` 的额外类定义
   * 确保文件中只有一个继承自`Tool`的类

3. **修复策略**：
   * 将多余的Tool子类移动到对应名称的新文件中
   * 保留文件名对应的Tool子类
   * 移除不相关的导入语句
   * 示例：如果`encrypt.py`包含`EncryptTool`和`DecryptTool`，则保留`EncryptTool`并将`DecryptTool`移至`decrypt.py`

4. **代码审查检查点**：
   * 每个工具文件只应包含**一个**`class XxxTool(Tool):`定义
   * 导入语句应只引入该工具类需要的依赖
   * 所有引用的工具函数名称应该与其定义完全一致## 进度记录管理

### 进度文件结构与维护

1. **创建进度文件**：
   * 首次交互时在`working/`目录创建`progress.md`
   * 每次新会话开始时首先检查并更新此文件

2. **进度文件内容结构**：
   ```markdown
   # 项目进度记录

   ## 项目概述
   [插件名称、类型和主要功能简介]

   ## 当前状态
   [描述项目当前所处阶段]

   ## 已完成工作
   - [时间] 完成了xxx功能
   - [时间] 实现了xxx

   ## 待办事项
   - [ ] 实现xxx功能
   - [ ] 完成xxx配置

   ## 问题与解决方案
   - 问题：xxx
     解决方案：xxx

   ## 技术决策记录
   - 决定使用xxx库，原因是xxx
   ```

3. **更新规则**：
   * **每次对话开始**时进行状态检查和记录更新
   * **每次完成任务**后添加到已完成工作列表
   * **每次遇到并解决问题**时记录在问题与解决方案部分
   * **每次确定技术方向**时记录在技术决策记录部分

4. **更新内容示例**：
   ````markdown
   ## 已完成工作
   - [2025-04-19 14:30] 完成了TOTP验证工具的基本实现
   - [2025-04-19 15:45] 添加了错误处理逻辑

   ## 待办事项
   - [ ] 实现secret_generator工具
   - [ ] 完善README文档
   ```# Dify插件开发助手
   ````

## 文件结构详解

```
your_plugin/
├── _assets/             # 图标和视觉资源
├── provider/            # 提供者定义和验证
│   ├── your_plugin.py   # 凭证验证逻辑
│   └── your_plugin.yaml # 提供者配置
├── tools/               # 工具实现
│   ├── your_plugin.py   # 工具功能实现
│   └── your_plugin.yaml # 工具参数和描述
├── utils/               # (可选) 辅助函数
├── working/             # 进度记录和工作文件
├── .env.example         # 环境变量模板
├── main.py              # 入口文件
├── manifest.yaml        # 插件主配置
├── README.md            # 文档
└── requirements.txt     # 依赖列表
```

### 文件位置与组织原则

1. **Python文件位置指导**：
   * 当用户提供单个Python文件时，应先检查其功能性质
   * 通用工具函数应放在`utils/`目录下
   * 具体工具实现应放在`tools/`目录下
   * 凭证验证逻辑应放在`provider/`目录下

2. **代码复制而非从头编写**：
   * 创建新文件时，优先通过复制现有文件作为模板，然后进行修改
   * 使用命令如：`cp tools/existing_tool.py tools/new_tool.py`
   * 这样可确保文件格式和结构符合框架要求

3. **保持框架一致性**：
   * 不随意修改文件结构
   * 不添加框架未定义的新文件类型
   * 遵循既定的命名约定

## 关键文件配置详解

### manifest.yaml

插件的主配置文件，定义了插件的基本信息和元数据。请遵循以下重要原则：

1. **保留已有内容**：
   * 不要删除配置文件中已有的项目，尤其是i18n相关部分
   * 以实际已有代码为基准进行修改和添加

2. **关键字段指导**：
   * **name**：不要修改此字段，它是插件的唯一标识符
   * **label**：建议完善多语言显示名称
   * **description**：建议完善多语言描述
   * **tags**：只能使用以下预定义的标签（每个插件只能选择1-2个最相关的标签）：
     ```
     'search', 'image', 'videos', 'weather', 'finance', 'design', 
     'travel', 'social', 'news', 'medical', 'productivity', 
     'education', 'business', 'entertainment', 'utilities', 'other'
     ```

3. **保持结构稳定**：
   * 除非有特殊需求，不要修改`resource`、`meta`、`plugins`等部分
   * 不要更改`type`和`version`等基础字段

```yaml
version: 0.0.1
type: plugin
author: your_name
name: your_plugin_name  # 不要修改此字段
label:
  en_US: Your Plugin Display Name
  zh_Hans: 你的插件显示名称
description:
  en_US: Detailed description of your plugin functionality
  zh_Hans: 插件功能的详细描述
icon: icon.svg
resource:
  memory: 268435456  # 256MB
  permission: {}
plugins:
  tools:
    - provider/your_plugin.yaml
meta:
  version: 0.0.1
  arch:
    - amd64
    - arm64
  runner:
    language: python
    version: "3.12"
    entrypoint: main
created_at: 2025-04-19T00:00:00.000000+08:00
privacy: PRIVACY.md
tags:
  - utilities  # 只使用预定义的标签
```

### provider/your\_plugin.yaml

提供者配置文件，定义了插件所需的凭证和工具列表：

1. **保留关键标识**：
   * **name**：不要修改此字段，保持与manifest.yaml中的name一致
   * 保留已有的i18n配置和结构

2. **完善显示信息**：
   * **label**：建议完善多语言显示名称
   * **description**：建议完善多语言描述

3. **添加新工具**：
   * 在`tools`列表中添加对新工具YAML文件的引用
   * 注意保持路径正确：`tools/feature_name.yaml`

```yaml
identity:
  author: your_name
  name: your_plugin_name  # 不要修改此字段
  label:
    en_US: Your Plugin Display Name
    zh_Hans: 你的插件显示名称
  description:
    en_US: Detailed description of your plugin functionality
    zh_Hans: 插件功能的详细描述
  icon: icon.svg
credentials_for_provider:  # 仅在需要API密钥等凭证时添加
  api_key:
    type: secret-input
    required: true
    label:
      en_US: API Key
      zh_Hans: API密钥
    placeholder:
      en_US: Enter your API key
      zh_Hans: 输入你的API密钥
    help:
      en_US: How to get your API key
      zh_Hans: 如何获取API密钥
    url: https://example.com/get-api-key
tools:  # 工具列表，添加新工具时在此更新
  - tools/feature_one.yaml
  - tools/feature_two.yaml
extra:
  python:
    source: provider/your_plugin.py
```

### tools/feature.yaml

工具配置文件，定义了工具的参数和描述：

1. **保留标识与结构**：
   * **name**：工具的唯一标识，与文件名相对应
   * 保持与现有文件结构一致

2. **完善配置内容**：
   * **label**和**description**：提供清晰的多语言显示内容
   * **parameters**：详细定义工具参数及其属性

3. **参数定义指导**：
   * **type**：选择适当的参数类型（string/number/boolean/file）
   * **form**：设置为`llm`（由AI提取）或`form`（UI配置）
   * **required**：明确是否为必需参数

```yaml
identity:
  name: feature_name  # 与文件名对应
  author: your_name
  label:
    en_US: Feature Display Name
    zh_Hans: 功能显示名称
description:
  human:  # 给人类用户看的描述
    en_US: Description for human users
    zh_Hans: 面向用户的功能描述
  llm: Description for AI models to understand when to use this tool.  # 给AI看的描述
parameters:  # 参数定义
  - name: param_name
    type: string  # string, number, boolean, file等
    required: true
    label:
      en_US: Parameter Display Name
      zh_Hans: 参数显示名称
    human_description:
      en_US: Parameter description for users
      zh_Hans: 面向用户的参数描述
    llm_description: Detailed parameter description for AI models
    form: llm  # llm表示可由AI从用户输入中提取，form表示需要在UI中配置
  # 其他参数...
extra:
  python:
    source: tools/feature.py  # 对应的Python实现文件
# 可选：定义输出的JSON Schema
output_schema:
  type: object
  properties:
    result:
      type: string
      description: Description of the result
```

### tools/feature.py

工具实现类，包含核心业务逻辑：

1. **类名与文件名对应**：
   * 类名遵循`FeatureTool`模式，与文件名相对应
   * 确保一个文件中**只有一个**Tool子类

2. **参数处理最佳实践**：
   * 对于必需参数，使用`.get()`方法并提供默认值：`param = tool_parameters.get("param_name", "")`

   * 对于可选参数，有两种处理方式：

     ```python
     # 方法1: 使用.get()方法（推荐用于单个参数）
     optional_param = tool_parameters.get("optional_param")  # 如果不存在返回None

     # 方法2: 使用try-except（处理多个可选参数）
     try:
         name = tool_parameters["name"]
         issuer_name = tool_parameters["issuer_name"]
     except KeyError:
         name = None
         issuer_name = None
     ```

   * 这种try-except方式是当前处理多个可选参数的临时解决方案

   * 始终在使用参数前验证其存在性和有效性

3. **输出方式**：
   * 使用`yield`返回各种类型的消息
   * 支持文本、JSON、链接和变量输出

```python
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# 导入工具函数，确保函数名称拼写正确
from utils.helpers import process_data

class FeatureTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # 1. 获取必需参数
            param = tool_parameters.get("param_name", "")
            
            # 2. 获取可选参数 - 使用try-except方式
            try:
                optional_param1 = tool_parameters["optional_param1"]
                optional_param2 = tool_parameters["optional_param2"]
            except KeyError:
                optional_param1 = None
                optional_param2 = None
                
            # 另一种可选参数获取方式 - 使用.get()方法
            another_optional = tool_parameters.get("another_optional")  # 如果不存在返回None
            
            # 3. 验证必需参数
            if not param:
                yield self.create_text_message("Parameter is required.")
                return
                
            # 4. 实现业务逻辑
            result = self._process_data(param, optional_param1, optional_param2)
            
            # 5. 返回结果
            # 文本输出
            yield self.create_text_message(f"Processed result: {result}")
            # JSON输出
            yield self.create_json_message({"result": result})
            # 变量输出 (用于工作流)
            yield self.create_variable_message("result_var", result)
                
        except Exception as e:
            # 错误处理
            yield self.create_text_message(f"Error: {str(e)}")
            
    def _process_data(self, param: str, opt1=None, opt2=None) -> str:
        """
        实现具体的业务逻辑
        
        Args:
            param: 必需的参数
            opt1: 可选参数1
            opt2: 可选参数2
            
        Returns:
            处理结果
        """
        # 根据参数是否存在执行不同的逻辑
        if opt1 and opt2:
            return f"Processed with all options: {param}, {opt1}, {opt2}"
        elif opt1:
            return f"Processed with option 1: {param}, {opt1}"
        elif opt2:
            return f"Processed with option 2: {param}, {opt2}"
        else:
            return f"Processed basic: {param}"
```

### utils/helper.py

辅助函数，实现可复用的功能逻辑：

1. **功能分离**：
   * 将通用功能抽取为单独的函数
   * 专注于单一职责
   * 注意函数命名的一致性（避免导入错误）

2. **错误处理**：
   * 包含适当的异常处理
   * 使用明确的异常类型
   * 提供有意义的错误消息

```python
import requests
from typing import Dict, Any, Optional

def call_external_api(endpoint: str, params: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    """
    调用外部API的通用函数
    
    Args:
        endpoint: API端点URL
        params: 请求参数
        api_key: API密钥
        
    Returns:
        API响应的JSON数据
    
    Raises:
        Exception: 如果API调用失败
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # 如果状态码不是200，抛出异常
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"API调用失败: {str(e)}")
```

### requirements.txt

依赖列表，指定插件所需的Python库：

1. **版本规范**：
   * 使用`~=`指定依赖版本范围
   * 避免过于宽松的版本要求

2. **必要依赖**：
   * 必须包含`dify_plugin`
   * 添加插件功能所需的所有第三方库

```
dify_plugin~=0.0.1b76
requests~=2.31.0
# 其他依赖...
```

## 工具开发最佳实践

### 1. 参数处理模式

1. **必需参数处理**：
   * 使用`.get()`方法并提供默认值：`param = tool_parameters.get("param_name", "")`
   * 验证参数有效性：`if not param: yield self.create_text_message("Error: Required parameter missing.")`

2. **可选参数处理**：
   * **单个可选参数**：使用`.get()`方法，允许返回None：`optional = tool_parameters.get("optional_param")`
   * **多个可选参数**：使用try-except模式处理KeyError：
     ```python
     try:
         param1 = tool_parameters["optional_param1"]
         param2 = tool_parameters["optional_param2"]
     except KeyError:
         param1 = None
         param2 = None
     ```
   * 这种try-except方式是当前处理多个可选参数的临时解决方案

3. **参数验证**：
   * 对必需参数进行验证：`if not required_param: return error_message`
   * 对可选参数进行条件处理：`if optional_param: do_something()`

### 2. 安全的文件操作方式

1. **避免本地文件读写**：
   * Dify插件运行在无服务器环境(如AWS Lambda)中，本地文件系统操作可能不可靠
   * 不要使用`open()`, `read()`, `write()`等直接文件操作
   * 不依赖本地文件作为状态存储

2. **使用内存或API替代**：
   * 临时数据使用内存变量存储
   * 持久化数据使用Dify提供的KV存储API
   * 对于大量数据，考虑使用数据库或云存储服务

### 3. 复制现有文件而非从头创建

对于不确定结构正确性的情况，强烈建议使用下列方法：

```bash
# 复制工具YAML文件作为模板
cp tools/existing_tool.yaml tools/new_tool.yaml

# 复制工具Python实现
cp tools/existing_tool.py tools/new_tool.py

# 同理适用于provider文件
cp provider/existing.yaml provider/new.yaml
```

这样可以确保文件结构和格式符合Dify插件框架的要求，然后再进行针对性修改。

### 4. 拆分工具功能

将复杂功能拆分为多个简单工具，每个工具专注于单一功能：

```
tools/
├── search.py          # 搜索功能
├── search.yaml
├── create.py          # 创建功能
├── create.yaml
├── update.py          # 更新功能
├── update.yaml
├── delete.py          # 删除功能
└── delete.yaml
```

### 2. 参数设计原则

* **必要性**：只要求必要的参数，提供合理默认值
* **类型定义**：选择合适的参数类型（string/number/boolean/file）
* **清晰描述**：为人类和AI提供清晰的参数描述
* **表单定义**：正确区分llm（AI提取）和form（UI配置）参数

### 3. 错误处理

```python
try:
    # 尝试执行操作
    result = some_operation()
    yield self.create_text_message("操作成功")
except ValueError as e:
    # 参数错误
    yield self.create_text_message(f"参数错误: {str(e)}")
except requests.RequestException as e:
    # API调用错误
    yield self.create_text_message(f"API调用失败: {str(e)}")
except Exception as e:
    # 其他未预期错误
    yield self.create_text_message(f"发生错误: {str(e)}")
```

### 4. 代码组织与复用

将可复用的逻辑抽取到utils目录：

```python
# 在工具实现中
from utils.api_client import ApiClient

class SearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        client = ApiClient(self.runtime.credentials["api_key"])
        results = client.search(tool_parameters["query"])
        yield self.create_json_message(results)
```

### 5. 输出格式

Dify支持多种输出格式：

```python
# 文本输出
yield self.create_text_message("这是文本消息")

# JSON输出
yield self.create_json_message({"key": "value"})

# 链接输出
yield self.create_link_message("https://example.com")

# 变量输出 (用于工作流)
yield self.create_variable_message("variable_name", "variable_value")
```

## 常见错误与解决方案

### 加载和初始化错误

1. **多个Tool子类错误**
   ```
   Exception: Multiple subclasses of Tool in /path/to/file.py
   ```
   * **原因**：同一个Python文件中定义了多个继承自Tool的类
   * **解决**：
     * 检查文件内容：`cat tools/problematic_file.py`
     * 每个文件保留一个与文件名对应的Tool子类
     * 将其他Tool子类移至对应的单独文件

2. **导入错误**
   ```
   ImportError: cannot import name 'x' from 'module'. Did you mean: 'y'?
   ```
   * **原因**：导入的函数名与实际定义不匹配
   * **解决**：
     * 检查utils中的函数名称：`cat utils/the_module.py`
     * 修正导入语句中的拼写错误
     * 注意函数名中的下划线、大小写等

3. **凭证验证失败**
   ```
   ToolProviderCredentialValidationError: Invalid API key
   ```
   * **原因**：凭证验证逻辑失败
   * **解决**：
     * 检查`_validate_credentials`方法实现
     * 确保API密钥格式正确
     * 添加详细的错误提示信息

### 运行时错误

1. **参数获取错误**
   ```
   KeyError: 'parameter_name'
   ```
   * **原因**：尝试访问不存在的参数
   * **解决**：
     * 使用`get()`代替直接索引：`param = tool_parameters.get("param_name", "")`
     * 确保参数名与YAML定义一致
     * 添加参数存在性检查

2. **API调用错误**
   ```
   requests.exceptions.RequestException: Connection error
   ```
   * **原因**：外部API调用失败
   * **解决**：
     * 添加超时参数：`timeout=10`
     * 使用`try/except`捕获异常
     * 实现重试逻辑

3. **执行超时**
   ```
   TimeoutError: Function execution timed out
   ```
   * **原因**：操作耗时过长
   * **解决**：
     * 优化API调用
     * 分解复杂操作为多个步骤
     * 设置合理的超时限制

### 配置和打包错误

1. **YAML格式错误**
   ```
   yaml.YAMLError: mapping values are not allowed in this context
   ```
   * **原因**：YAML格式不正确
   * **解决**：
     * 检查缩进（使用空格而非制表符）
     * 确保冒号后有空格
     * 使用YAML验证器检查

2. **打包失败**
   ```
   Error: Failed to pack plugin
   ```
   * **原因**：文件结构或依赖问题
   * **解决**：
     * 检查manifest.yaml配置
     * 确保所有引用的文件存在
     * 审查requirements.txt内容

## 代码示例：TOTP工具

以下是一个完整的TOTP (Time-based One-Time Password) 插件示例，展示了良好的代码组织和最佳实践：

### utils/totp\_verify.py

```python
import pyotp
import time

def verify_totp(secret_key, totp_code, offset=5, strict=False):
    """
    验证基于时间的一次性密码(TOTP)。
    
    Args:
        secret_key: 用于生成TOTP的密钥或配置URL
        totp_code: 用户提交的动态令牌
        offset: 允许提前或延迟验证的秒数
        strict: 是否使用严格验证(仅在精确匹配时返回成功)
        
    Returns:
        包含以下内容的字典:
        - 'status': 'success' 或 'fail'
        - 'detail': 内部消息(不面向终端用户)
    """
    try:
        # 检测是否为配置URL
        if secret_key.startswith('otpauth://'):
            totp = pyotp.parse_uri(secret_key)
        else:
            totp = pyotp.TOTP(secret_key)
            
        current_time = time.time()

        # 精确时间验证
        if totp.verify(totp_code):
            return {'status': 'success', 'detail': 'Token is valid'}

        # 偏移验证
        early_valid = totp.verify(totp_code, for_time=current_time + offset)
        late_valid = totp.verify(totp_code, for_time=current_time - offset)
        off_time_valid = early_valid or late_valid

        detail_message = (
            f"Token is valid but not on time. "
            f"{'Early' if early_valid else 'Late'} within {offset} seconds"
            if off_time_valid else
            "Token is invalid"
        )

        if strict:
            return {'status': 'fail', 'detail': detail_message}
        else:
            return (
                {'status': 'success', 'detail': detail_message}
                if off_time_valid
                else {'status': 'fail', 'detail': detail_message}
            )
    except Exception as e:
        return {'status': 'fail', 'detail': f'Verification error: {str(e)}'}
```

### tools/totp.yaml

```yaml
identity:
  name: totp
  author: your-name
  label:
    en_US: TOTP Validator
    zh_Hans: TOTP 验证器
description:
  human:
    en_US: Time-based one-time password (TOTP) validator
    zh_Hans: 基于时间的一次性密码 (TOTP) 验证器
  llm: Time-based one-time password (TOTP) validator, this tool is used to validate a 6 digit TOTP code with a secret key or provisioning URI.
parameters:
  - name: secret_key
    type: string
    required: true
    label:
      en_US: TOTP secret key or provisioning URI
      zh_Hans: TOTP 私钥或 URI
    human_description:
      en_US: The secret key or provisioning URI used to generate the TOTP
      zh_Hans: 用于生成 TOTP 的私钥或 URI
    llm_description: The secret key or provisioning URI (starting with 'otpauth://') used to generate the TOTP, this is highly sensitive and should be kept secret.
    form: llm
  - name: user_code
    type: string
    required: true
    label:
      en_US: 6 digit TOTP code to validate
      zh_Hans: 要验证的 6 位 TOTP 代码
    human_description:
      en_US: 6 digit TOTP code to validate
      zh_Hans: 要验证的 6 位 TOTP 代码
    llm_description: 6 digit TOTP code to validate
    form: llm
extra:
  python:
    source: tools/totp.py
output_schema:
  type: object
  properties:
    True_or_False:
      type: string
      description: Whether the TOTP is valid or not, return in string format, "True" or "False".
```

### tools/totp.py

```python
from collections.abc import Generator
from typing import Any

# 正确导入工具函数
from utils.totp_verify import verify_totp

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# 一个文件只包含一个Tool子类
class TotpTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """验证基于时间的一次性密码(TOTP)"""
        # 获取参数，使用get()避免KeyError
        secret_key = tool_parameters.get("secret_key")
        totp_code = tool_parameters.get("user_code")
        
        # 参数验证
        if not secret_key:
            yield self.create_text_message("Error: Secret key is required.")
            return
        if not totp_code:
            yield self.create_text_message("Error: TOTP code is required.")
            return
        
        try:
            # 调用工具函数
            result = verify_totp(secret_key, totp_code)
            
            # 返回结果
            yield self.create_json_message(result)
            
            # 基于验证结果返回不同的消息
            if result["status"] == "success":
                yield self.create_text_message("Valid")
                yield self.create_variable_message("True_or_False", "True")
            else:
                yield self.create_text_message("Invalid")
                yield self.create_variable_message("True_or_False", "False")
                
        except Exception as e:
            # 错误处理
            yield self.create_text_message(f"Verification error: {str(e)}")
```

### tools/secret\_generator.py

```python
from collections.abc import Generator
from typing import Any

import pyotp

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# 注意：一个文件只包含一个Tool子类
class SecretGenerator(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """生成TOTP密钥"""
        try:
            # 生成随机密钥
            secret_key = pyotp.random_base32()
            yield self.create_text_message(secret_key)
            
            # 安全获取可选参数
            name = tool_parameters.get("name")
            issuer_name = tool_parameters.get("issuer_name")
            
            # 如果提供了名称或发行方，生成配置URI
            if name or issuer_name:
                provisioning_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(
                    name=name, 
                    issuer_name=issuer_name
                )
                yield self.create_variable_message("provisioning_uri", provisioning_uri)
                
        except Exception as e:
            yield self.create_text_message(f"Error generating secret: {str(e)}")
```

### requirements.txt

```
dify_plugin~=0.0.1b76
pyotp~=2.9.0
```

这个示例展示了:

* 清晰的功能分离（utils中的工具函数，tools中的工具类）
* 良好的错误处理和参数验证
* 一个文件只包含一个Tool子类
* 详细的注释和文档字符串
* 精心设计的YAML配置
