# Python 代码风格指南

本项目遵循 Python PEP 8 代码风格规范。

## 编码规范

### 1. 命名规范

- **类名**: 使用大驼峰命名法 (CamelCase)
- **函数和变量**: 使用小写 + 下划线 (snake_case)
- **常量**: 使用全大写 + 下划线
- **私有方法/变量**: 使用单下划线前缀

### 2. 代码格式

- **缩进**: 使用 4 个空格（不使用 Tab）
- **行宽**: 最大 100 字符
- **空行**:
  - 函数之间空 2 行
  - 类中方法之间空 1 行

### 3. 导入规范

```python
# 标准库
import os
import sys

# 第三方库
import pandas as pd
import numpy as np

# 本地模块
from .local_module import MyClass
```

### 4. 文档字符串

所有公共函数和类都应包含文档字符串：

```python
def calculate_average(numbers):
    """计算数字列表的平均值。

    Args:
        numbers: 数字列表

    Returns:
        平均值（float）
    """
    return sum(numbers) / len(numbers)
```

## 自动化工具

### 使用 Black 格式化代码

```bash
pip install black
black .
```

### 使用 Flake8 检查代码

```bash
pip install flake8
flake8 .
```

## VS Code 配置

在 `.vscode/settings.json` 中添加：

```json
{
    "python.formatting.provider": "black",
    "python.linting.flake8Enabled": true,
    "editor.formatOnSave": true,
    "editor.rulers": [100]
}
```
