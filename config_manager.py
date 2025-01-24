import json
import os
import sys
import json
from config import DEFAULT_FORM_DATA

CONFIG_FILE = 'form_config.json'

def load_config():
    """加载配置文件，如果不存在则返回默认值"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return DEFAULT_FORM_DATA.copy()
    except Exception:
        return DEFAULT_FORM_DATA.copy()

def save_config(config_data):
    """保存配置到文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)
        return True
    except Exception:
        return False 
