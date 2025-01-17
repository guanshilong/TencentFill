# 腾讯云表单自动填写工具

一个用于自动填写腾讯云表单的桌面应用程序。

## 项目结构

form-auto-fill/
├── src/
│ ├── form_filler.py # 主程序文件
│ └── form_template.html # 表单模板文件（用于开发参考）
├── requirements.txt # 项目依赖
└── README.md # 项目说明文档

## 注意事项

1. 使用前请确保已安装Chrome浏览器
2. 需要稳定的网络连接
3. 如需修改预设数据，请修改源代码中的form_data字典

## 依赖要求

- Python 3.6+
- selenium
- tkinter (Python标准库)
- Chrome浏览器
- ChromeDriver (与Chrome版本匹配)

## requirements.txt
    selenium>=4.0.0
    pyinstaller>=5.0.0

```bash
pip install -r requirements.txt
```

## 打包命令

### Windows系统打包命令

```bash
cd TencentFill
# 基础打包
pyinstaller --windowed --name "表单填写工具" form_filler.py
# 单文件打包（推荐）
pyinstaller --windowed --onefile --name "表单填写工具" form_filler.py
# 添加图标打包
pyinstaller --windowed --onefile --icon=icon.ico --name "表单填写工具" form_filler.py
```

### Mac系统打包命令

```bash
cd TencentFill
# 基础打包
pyinstaller --windowed --name "表单填写工具" form_filler.py
# 单文件打包（推荐）
pyinstaller --windowed --onefile --name "表单填写工具" form_filler.py
# 添加图标打包
pyinstaller --windowed --onefile --icon=icon.icns --name "表单填写工具" form_filler.py
```

### 打包参数说明

- `--windowed`: 创建一个不显示命令行窗口的GUI应用
- `--onefile`: 将所有依赖打包成单个可执行文件
- `--name`: 指定生成的可执行文件名称
- `--icon`: 指定应用程序图标（可选）
- `--clean`: 清理临时文件（可选）

## 使用说明

1. 运行打包后的可执行文件
2. 在输入框中输入或确认表单URL
3. 点击"开始填写"按钮
4. 程序会自动填写预设的表单信息

## 预设表单数据
