# build.py
import PyInstaller.__main__
import os
import sys

def get_resource_path(relative_path):
    """获取资源的绝对路径"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 确保data目录存在
if not os.path.exists('data'):
    os.makedirs('data')

app_name = "wechat-multi-open"
icon_path = "data/wechat.ico" if os.path.exists("data/wechat.ico") else None

pack_cmd = [
    'main.py',
    f'--name={app_name}',
    '--onefile',
    '--windowed',
    '--noconsole',
    
    # 添加数据文件
    '--add-data=data;data',
    '--add-data=data/wechat.ico;data' if icon_path else '',
    
    # 必须的隐藏导入
    '--hidden-import=webview',
    '--hidden-import=flask',
    '--hidden-import=pystray',
    '--hidden-import=PIL',
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=jinja2',
    '--hidden-import=werkzeug',
    '--hidden-import=pywin32',
    
    # WebView特殊处理
    '--collect-all=webview',
    
    # 清理和优化
    '--clean',
    '--noconfirm',
    
    # 防止临时文件问题
    '--runtime-tmpdir=.'
]

# 添加图标（如果存在）
if icon_path:
    pack_cmd.append(f'--icon={icon_path}')

# 移除空参数
pack_cmd = [x for x in pack_cmd if x]

PyInstaller.__main__.run(pack_cmd)