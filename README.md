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
pip install PyQt6
pip install selenium
```

### ChromeDriver安装

1. 确保已安装Chrome浏览器
2. 下载与Chrome浏览器版本匹配的[ChromeDriver](https://sites.google.com/chromium.org/driver/)
3. 将ChromeDriver放入系统PATH路径中

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

## 注意事项

1. 确保Chrome浏览器已正确安装
2. 确保网络连接正常
3. 首次使用需要修改默认地址
4. 程序会自动保存修改后的地址信息

## 常见问题

1. 无法启动Chrome浏览器
   - 检查Chrome是否正确安装
   - 确认ChromeDriver版本是否匹配

2. 表单填写失败
   - 检查网络连接
   - 确认URL是否正确
   - 确认表单页面是否加载完成

## 开发说明

本项目使用以下技术栈：
- PyQt6: 用于构建图形界面
- Selenium: 用于自动化表单填写
- JSON: 用于配置文件存储

## 许可证

© 2025 Form Auto-Fill Tool. All rights reserved.
