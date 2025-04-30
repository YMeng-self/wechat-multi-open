import PyInstaller.__main__
import os
import shutil
from PIL import Image, ImageDraw

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 确保uploads目录存在
uploads_dir = os.path.join(current_dir, 'uploads')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

# 创建图标
def create_icon():
    # 创建一个256x256的图标
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制背景圆
    draw.ellipse([(20, 20), (236, 236)], fill=(52, 152, 219, 255))
    
    # 绘制微信图标
    # 绘制外圈
    draw.ellipse([(60, 60), (196, 196)], fill=(255, 255, 255, 255))
    # 绘制内圈
    draw.ellipse([(80, 80), (176, 176)], fill=(52, 152, 219, 255))
    # 绘制两个小圆
    draw.ellipse([(100, 100), (120, 120)], fill=(255, 255, 255, 255))
    draw.ellipse([(136, 100), (156, 120)], fill=(255, 255, 255, 255))
    # 绘制笑脸
    draw.arc([(100, 130), (156, 160)], 0, 180, fill=(255, 255, 255, 255), width=5)
    
    # 保存图标
    icon_path = os.path.join(current_dir, 'wechat_icon.ico')
    img.save(icon_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    return icon_path

# 创建图标
icon_path = create_icon()

# 定义打包参数
PyInstaller.__main__.run([
    'wechat_multi_open_web.py',
    '--name=wechat-multi-open',
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