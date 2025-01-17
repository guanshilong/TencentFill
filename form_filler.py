from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

class FormFiller:
    def __init__(self):
        # 初始化Chrome浏览器
        self.driver = webdriver.Chrome()
        
    def fill_form(self, url):
        # 预定义的表单数据
        form_data = {
            'nickname': '测试昵称',
            'name': '张三',
            'phone': '13800138000',
            'address': '广东省深圳市南山区腾讯大厦'
        }
        
        try:
            # 打开网页
            self.driver.get(url)
            
            # 等待页面加载
            wait = WebDriverWait(self.driver, 10)
            
            # 填写社区昵称
            nickname_input = wait.until(EC.presence_of_element_located((By.NAME, "7lap1mcqwr7")))
            nickname_input.send_keys(form_data['nickname'])
            
            # 填写姓名
            name_input = self.driver.find_element(By.NAME, "xepe2botxth")
            name_input.send_keys(form_data['name'])
            
            # 填写电话号码
            phone_input = self.driver.find_element(By.NAME, "tvvoz8pt5tf")
            phone_input.send_keys(form_data['phone'])
            
            # 填写收货信息
            address_input = self.driver.find_element(By.NAME, "f54spd7ug5q")
            address_input.send_keys(form_data['address'])
            
            # 勾选同意协议
            checkbox = self.driver.find_element(By.CLASS_NAME, "f-checkbox")
            if not checkbox.is_selected():
                checkbox.click()
            
            # 等待几秒确保表单填写完成
            time.sleep(2)
            messagebox.showinfo("提示", "表单填写完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"填写表单时发生错误: {str(e)}")
        finally:
            self.driver.quit()

class FormFillerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("腾讯云表单自动填写工具")
        self.window.geometry("500x250")
        self.window.configure(bg='#f0f0f0')
        
        # 设置字体
        self.title_font = Font(family="Microsoft YaHei", size=14, weight="bold")
        self.normal_font = Font(family="Microsoft YaHei", size=10)
        
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(
            main_frame, 
            text="表单自动填写工具", 
            font=self.title_font,
            foreground="#333333",
            background="#f0f0f0"
        )
        title_label.pack(pady=(0, 20))
        
        # URL输入框架
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 20))
        
        url_label = tk.Label(
            url_frame,
            text="请输入表单URL:",
            font=self.normal_font,
            background="#f0f0f0"
        )
        url_label.pack(anchor='w', pady=(0, 5))
        
        # 设置URL输入框样式
        style = ttk.Style()
        style.configure(
            "URL.TEntry",
            padding=5,
            relief="flat"
        )
        
        self.url_entry = ttk.Entry(
            url_frame,
            width=50,
            style="URL.TEntry",
            font=self.normal_font
        )
        self.url_entry.pack(fill=tk.X)
        self.url_entry.insert(0, "https://cloud.tencent.com/apply/p/q067igrhxh")
        
        # 状态提示
        self.status_label = tk.Label(
            main_frame,
            text="准备就绪",
            font=self.normal_font,
            foreground="#666666",
            background="#f0f0f0"
        )
        self.status_label.pack(pady=10)
        
        # 提交按钮
        style.configure(
            "Submit.TButton",
            padding=10,
            font=self.normal_font
        )
        
        submit_button = ttk.Button(
            main_frame,
            text="开始填写",
            style="Submit.TButton",
            command=self.start_fill
        )
        submit_button.pack(pady=10)
        
        # 版权信息
        copyright_label = tk.Label(
            main_frame,
            text="© 2024 Form Auto-Fill Tool",
            font=("Microsoft YaHei", 8),
            foreground="#999999",
            background="#f0f0f0"
        )
        copyright_label.pack(side=tk.BOTTOM, pady=10)
        
        # 使窗口居中显示
        self.center_window()
        
    def center_window(self):
        """使窗口在屏幕中央显示"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def start_fill(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("错误", "请输入URL！")
            return
        
        self.status_label.config(text="正在填写表单...", foreground="#1E90FF")
        self.window.update()
        
        try:
            form_filler = FormFiller()
            form_filler.fill_form(url)
            self.status_label.config(text="表单填写完成！", foreground="#32CD32")
        except Exception as e:
            self.status_label.config(text="填写失败！", foreground="#FF4500")
            messagebox.showerror("错误", str(e))
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = FormFillerGUI()
    app.run() 