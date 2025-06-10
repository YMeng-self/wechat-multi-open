import PyInstaller.__main__
import os
import shutil
from PIL import Image

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 确保uploads目录存在
uploads_dir = os.path.join(current_dir, 'uploads')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

# 创建图标
try:
    # 替换为你的图标路径
    icon_path = Image.open("icon/wechat.ico")  
except FileNotFoundError:
    # 如果没有图标，创建一个默认的
    icon_path = Image.new('RGB', (64, 64), color='blue')

# 定义打包参数
app_name = "wechat-multi-open"
PyInstaller.__main__.run([
    'wechat_multi_open.py',
    f'--name={app_name}',
    '--onefile',
    '--windowed',
    '--add-data=uploads;uploads',
    '--add-data=wechat_config.json;.',
    f'--icon={icon_path}',
    '--hidden-import=pystray',
    '--hidden-import=PIL',
    '--hidden-import=PIL._tkinter_finder',
    '--clean',
    '--noconfirm'
])

# 复制配置文件到dist目录
dist_dir = os.path.join(current_dir, 'dist')
if os.path.exists(dist_dir):
    config_file = os.path.join(current_dir, 'wechat_config.json')
    if os.path.exists(config_file):
        shutil.copy2(config_file, dist_dir)
    
    # 删除临时图标文件
    if os.path.exists(icon_path):
        os.remove(icon_path) 