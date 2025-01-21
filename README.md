# 腾讯云表单自动填写工具

一个用于自动填写腾讯云表单的桌面应用程序，使用Python和PyQt6开发。

## 功能特点

- 自动填写表单信息
- 保存和管理收货地址
- 现代化的图形界面
- 支持查看和修改地址信息
- 自动记住上次填写的信息

## 安装说明

### 环境要求

- Python 3.8+
- Chrome浏览器
- ChromeDriver

### 依赖安装

```bash
# 安装所需的Python包
pip install -r requirements.txt
```

### ChromeDriver安装

1. 确保已安装Chrome浏览器
2. 下载与Chrome浏览器版本匹配的[ChromeDriver](https://sites.google.com/chromium.org/driver/)
3. 将ChromeDriver放入系统PATH路径中

## 打包说明

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv_build

# 激活虚拟环境
# Windows:
.\venv_build\Scripts\activate
# macOS/Linux:
source venv_build/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 打包命令

#### Windows系统
```bash
# 使用spec文件打包（推荐）
pyinstaller 表单填写工具.spec

# 或使用build.py打包
python build.py

# 或直接打包
pyinstaller --clean --windowed --name "表单填写工具" form_filler.py
```

#### macOS系统
```bash
# 使用spec文件打包（推荐）
pyinstaller 表单填写工具.spec

# 或使用build.py打包
python build.py

# 或直接打包
pyinstaller --clean --windowed --name "表单填写工具" form_filler.py
```

### 3. 打包后的文件结构

```
dist/
├── 表单填写工具/          # 程序目录
│   ├── 表单填写工具.exe   # Windows可执行文件
│   └── ...              # 其他依赖文件
└── 表单填写工具.app/      # macOS应用包
```

## 使用说明

1. 首次运行
   - 启动程序后会提示修改默认地址信息
   - 必须修改默认地址才能继续使用

2. 日常使用
   - 点击"查看地址"可以查看当前保存的地址信息
   - 点击"修改地址"可以修改保存的地址信息
   - 在输入框中粘贴表单URL
   - 点击"开始填写"按钮自动填写表单

## 文件说明

- `form_filler.py`: 主程序文件
- `config.py`: 配置文件，包含默认表单数据
- `config_manager.py`: 配置管理模块
- `form_config.json`: 保存的配置文件
- `表单填写工具.spec`: PyInstaller打包配置文件
- `build.py`: 打包脚本
- `requirements.txt`: 项目依赖列表

## 开发说明

### 1. 开发环境设置
```bash
# 创建开发虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装开发依赖
pip install -r requirements.txt
```

### 2. 代码格式化
```bash
# 使用black格式化代码
black .

# 使用flake8检查代码
flake8
```

### 3. 运行测试
```bash
# 运行所有测试
pytest

# 运行单个测试文件
pytest tests/test_form_filler.py
```

## 常见问题

1. 无法启动Chrome浏览器
   - 检查Chrome是否正确安装
   - 确认ChromeDriver版本是否匹配
   - 检查ChromeDriver是否在PATH中

2. 表单填写失败
   - 检查网络连接
   - 确认URL是否正确
   - 确认表单页面是否加载完成

3. 打包问题
   - 确保在虚拟环境中打包
   - 检查所有依赖是否正确安装
   - 使用spec文件打包以确保配置正确

## 技术栈

- PyQt6: 用于构建图形界面
- Selenium: 用于自动化表单填写
- PyInstaller: 用于打包应用
- JSON: 用于配置文件存储

## 许可证

© 2025 Form Auto-Fill Tool. All rights reserved.
