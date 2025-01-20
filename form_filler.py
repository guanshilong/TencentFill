import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import DEFAULT_FORM_DATA, FORM_LABELS
from config_manager import load_config, save_config

class FormDataDialog(QDialog):
    def __init__(self, parent=None, form_data=None, readonly=False):
        super().__init__(parent)
        self.form_data = form_data.copy() if form_data else DEFAULT_FORM_DATA.copy()
        self.readonly = readonly
        self.result = None
        self.setup_ui()
        
        # 添加电话号码验证
        if not readonly:
            phone_entry = self.entries.get('phone')
            if phone_entry:
                phone_entry.textChanged.connect(self.validate_phone)
                # 设置最大长度为11位
                phone_entry.setMaxLength(11)
    
    def setup_ui(self):
        self.setWindowTitle("查看地址" if self.readonly else "修改地址")
        self.setFixedSize(400, 300)
        
        layout = QFormLayout(self)
        layout.setSpacing(10)
        
        # 创建输入框
        self.entries = {}
        for key, label in FORM_LABELS.items():
            entry = QLineEdit(self.form_data[key])
            if self.readonly:
                entry.setReadOnly(True)
            entry.setMinimumWidth(250)
            layout.addRow(f"{label}:", entry)
            self.entries[key] = entry
        
        # 按钮布局
        button_layout = QHBoxLayout()
        if not self.readonly:
            save_btn = QPushButton("保存")
            save_btn.clicked.connect(self.accept)
            cancel_btn = QPushButton("取消")
            cancel_btn.clicked.connect(self.reject)
            button_layout.addWidget(save_btn)
            button_layout.addWidget(cancel_btn)
        else:
            close_btn = QPushButton("关闭")
            close_btn.clicked.connect(self.reject)
            button_layout.addWidget(close_btn)
        
        layout.addRow("", button_layout)

    def validate_phone(self, text):
        """验证电话号码格式"""
        phone_entry = self.entries.get('phone')
        if not phone_entry:
            return
            
        # 移除非数字字符
        text = ''.join(filter(str.isdigit, text))
        
        # 如果输入的不是数字，直接清除
        if text != phone_entry.text():
            phone_entry.setText(text)
        
        # 验证号码格式
        is_valid = len(text) == 11 and text.startswith(('13', '14', '15', '16', '17', '18', '19'))
        
        if text:  # 只有当有输入时才显示样式
            if is_valid:
                phone_entry.setStyleSheet("""
                    QLineEdit {
                        border: 1px solid #52c41a;
                        padding: 8px;
                        border-radius: 4px;
                        background-color: white;
                    }
                """)
            else:
                phone_entry.setStyleSheet("""
                    QLineEdit {
                        border: 1px solid #ff4d4f;
                        padding: 8px;
                        border-radius: 4px;
                        background-color: white;
                    }
                """)
    
    def accept(self):
        """保存前验证"""
        phone = self.entries['phone'].text()
        if not self._is_valid_phone(phone):
            QMessageBox.warning(
                self,
                "错误",
                "请输入正确的11位手机号码！",
                QMessageBox.StandardButton.Ok
            )
            self.entries['phone'].setFocus()
            return
            
        self.result = {
            key: entry.text()
            for key, entry in self.entries.items()
        }
        super().accept()
    
    def _is_valid_phone(self, phone):
        """验证电话号码是否有效"""
        if not phone:
            return False
        
        # 验证规则：
        # 1. 必须是11位数字
        # 2. 必须以1开头
        # 3. 第二位必须是3-9
        if not phone.isdigit():
            return False
        if len(phone) != 11:
            return False
        if not phone.startswith('1'):
            return False
        if phone[1] not in '3456789':
            return False
            
        return True

class FormFillerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.form_data = load_config()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("腾讯云表单自动填写工具")
        self.setFixedSize(500, 300)
        
        # 主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)  # 设置边距
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(15)  # 增加按钮间距
        
        # 创建按钮样式
        button_style = """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 100px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #e3e3e3;
                border: 1px solid #c0c0c0;
            }
            QPushButton:pressed {
                background-color: #d7d7d7;
            }
        """
        
        view_button = QPushButton("查看地址")
        view_button.clicked.connect(lambda: self.edit_form_data(True))
        edit_button = QPushButton("修改地址")
        edit_button.clicked.connect(lambda: self.edit_form_data(False))
        
        for btn in [view_button, edit_button]:
            btn.setStyleSheet(button_style)
            btn.setFont(QFont("Microsoft YaHei", 10))
            button_layout.addWidget(btn)
        
        layout.addLayout(button_layout)
        
        # URL输入框
        url_layout = QHBoxLayout()
        url_layout.setSpacing(10)
        
        url_label = QLabel("表单URL:")
        url_label.setFont(QFont("Microsoft YaHei", 10))
        url_label.setFixedWidth(80)
        
        self.url_entry = QLineEdit()
        self.url_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #a0a0a0;
            }
        """)
        self.url_entry.setFont(QFont("Microsoft YaHei", 10))
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_entry)
        layout.addLayout(url_layout)
        
        # 开始填写按钮
        submit_button = QPushButton("开始填写")
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 100px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
            QPushButton:pressed {
                background-color: #096dd9;
            }
        """)
        submit_button.setFont(QFont("Microsoft YaHei", 10))
        submit_button.clicked.connect(self.start_fill)
        layout.addWidget(submit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 版权信息
        copyright_label = QLabel("© 2025 Form Auto-Fill Tool")
        copyright_label.setFont(QFont("Microsoft YaHei", 8))
        copyright_label.setStyleSheet("color: #999999;")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)
        
        # 添加免责声明
        disclaimer_label = QLabel("仅做学习之用")
        disclaimer_label.setFont(QFont("Microsoft YaHei", 8))
        disclaimer_label.setStyleSheet("color: #999999;")
        disclaimer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(disclaimer_label)
        
        # 首次运行检查和提示
        QApplication.instance().processEvents()
        self.check_first_run()
    
    def check_first_run(self):
        """检查是否首次运行并处理"""
        # 检查是否使用默认配置
        is_default = all(
            self.form_data[key] == DEFAULT_FORM_DATA[key]
            for key in DEFAULT_FORM_DATA
        )
        
        if is_default:
            # 显示强制修改提示
            QMessageBox.information(
                self,
                "首次使用提示",
                "首次使用请修改收货地址",
                QMessageBox.StandardButton.Ok
            )
            
            # 强制打开修改对话框，直到用户修改了地址
            while is_default:
                dialog = FormDataDialog(self, self.form_data, readonly=False)
                if dialog.exec():
                    self.form_data = dialog.result
                    save_config(self.form_data)
                    
                    # 检查是否真的修改了
                    is_default = all(
                        self.form_data[key] == DEFAULT_FORM_DATA[key]
                        for key in DEFAULT_FORM_DATA
                    )
                    
                    if is_default:
                        QMessageBox.warning(
                            self,
                            "提示",
                            "请修改默认的收货地址信息！",
                            QMessageBox.StandardButton.Ok
                        )
                else:
                    # 用户点击取消，再次提醒
                    reply = QMessageBox.warning(
                        self,
                        "提示",
                        "首次使用必须修改默认地址，是否继续？",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.No:
                        sys.exit(0)  # 用户选择退出程序

    def edit_form_data(self, readonly=False):
        dialog = FormDataDialog(self, self.form_data, readonly)
        if dialog.exec():
            self.form_data = dialog.result
            if not readonly:
                save_config(self.form_data)

    def start_fill(self):
        url = self.url_entry.text()
        if not url:
            QMessageBox.warning(self, "错误", "请输入URL！")
            return
        
        try:
            form_filler = FormFiller()
            form_filler.fill_form(url, self.form_data)
            # 浏览器关闭后才显示完成提示
            QMessageBox.information(self, "提示", "表单填写完成！")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

class FormFiller:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome()
        except Exception as e:
            raise Exception(f"无法启动Chrome浏览器: {str(e)}")
    
    def fill_form(self, url, form_data):
        # 提交前验证电话号码
        if not self._validate_phone(form_data['phone']):
            raise Exception("电话号码格式不正确，请检查！")
            
        try:
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 10)
            
            try:
                # 只填写必填字段
                nickname_input = wait.until(EC.presence_of_element_located((By.NAME, "7lap1mcqwr7")))
                nickname_input.send_keys(form_data['nickname'])
                
                name_input = self.driver.find_element(By.NAME, "xepe2botxth")
                name_input.send_keys(form_data['name'])
                
                phone_input = self.driver.find_element(By.NAME, "tvvoz8pt5tf")
                phone_input.send_keys(form_data['phone'])
                
                address_input = self.driver.find_element(By.NAME, "f54spd7ug5q")
                address_input.send_keys(form_data['address'])
                
                # 勾选协议复选框
                checkbox = self.driver.find_element(By.CLASS_NAME, "f-checkbox")
                if not checkbox.is_selected():
                    checkbox.click()
                
                # 等待浏览器关闭
                while True:
                    try:
                        # 检查浏览器是否还在运行
                        self.driver.current_url
                        time.sleep(1)
                    except:
                        break
                
            except Exception as e:
                raise Exception(f"填写表单时发生错误: {str(e)}")
            
        finally:
            try:
                self.driver.quit()
            except:
                pass

    def _validate_phone(self, phone):
        """验证电话号码格式"""
        if not phone:
            return False
            
        # 验证规则：
        # 1. 必须是11位数字
        # 2. 必须以1开头
        # 3. 第二位必须是3-9
        if not phone.isdigit():
            return False
        if len(phone) != 11:
            return False
        if not phone.startswith('1'):
            return False
        if phone[1] not in '3456789':
            return False
            
        return True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle("Fusion")
    
    window = FormFillerGUI()
    window.show()
    
    sys.exit(app.exec()) 