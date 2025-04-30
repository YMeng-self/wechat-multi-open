import PyInstaller.__main__
import os
import shutil

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 确保uploads目录存在
uploads_dir = os.path.join(current_dir, 'uploads')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

# 定义打包参数
PyInstaller.__main__.run([
    'wechat_multi_open_web.py',
    '--name=wechat-multi-open',
    '--onefile',
    '--windowed',
    '--add-data=uploads;uploads',
    '--add-data=wechat_config.json;.',
    '--icon=NONE',
    '--clean',
    '--noconfirm'
])

# 复制配置文件到dist目录
dist_dir = os.path.join(current_dir, 'dist')
if os.path.exists(dist_dir):
    config_file = os.path.join(current_dir, 'wechat_config.json')
    if os.path.exists(config_file):
        shutil.copy2(config_file, dist_dir) 