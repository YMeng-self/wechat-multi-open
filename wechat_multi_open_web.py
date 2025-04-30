from flask import Flask, render_template_string, request, send_from_directory
import os
import subprocess
import sys
import json
import webbrowser
import threading
import time
import pystray
from PIL import Image, ImageDraw

app = Flask(__name__)

# 配置文件路径
CONFIG_FILE = "wechat_config.json"

# 默认微信安装路径
DEFAULT_WECHAT_PATHS = [
    r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
    r"C:\Program Files\Tencent\WeChat\WeChat.exe",
    r"D:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
    r"D:\Program Files\Tencent\WeChat\WeChat.exe"
]

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"wechat_path": "", "count": 2}
    return {"wechat_path": "", "count": 2}

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def get_default_wechat_path():
    """获取默认微信路径"""
    config = load_config()
    if config["wechat_path"] and os.path.exists(config["wechat_path"]):
        return config["wechat_path"]
    
    for path in DEFAULT_WECHAT_PATHS:
        if os.path.exists(path):
            return path
    return ""

def create_icon():
    """创建系统托盘图标"""
    # 创建一个简单的图标
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制背景圆
    draw.ellipse([(4, 4), (60, 60)], fill=(52, 152, 219, 255))
    
    # 绘制微信图标
    # 绘制外圈
    draw.ellipse([(16, 16), (48, 48)], fill=(255, 255, 255, 255))
    # 绘制内圈
    draw.ellipse([(20, 20), (44, 44)], fill=(52, 152, 219, 255))
    # 绘制两个小圆
    draw.ellipse([(24, 24), (28, 28)], fill=(255, 255, 255, 255))
    draw.ellipse([(36, 24), (40, 28)], fill=(255, 255, 255, 255))
    # 绘制笑脸
    draw.arc([(24, 32), (40, 40)], 0, 180, fill=(255, 255, 255, 255), width=2)
    
    return img

def on_quit(icon):
    """退出程序"""
    icon.stop()
    os._exit(0)

def setup_tray():
    """设置系统托盘"""
    icon = pystray.Icon("wechat_multi_open")
    icon.icon = create_icon()
    icon.title = "微信多开工具"
    icon.menu = pystray.Menu(
        pystray.MenuItem("打开网页", lambda: webbrowser.open('http://127.0.0.1:5000')),
        pystray.MenuItem("退出", on_quit)
    )
    icon.run()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>微信多开工具</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            max-width: 500px;
            width: 90%;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            font-size: 28px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #34495e;
            font-weight: bold;
        }
        input[type="text"], input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus, input[type="number"]:focus {
            border-color: #3498db;
            outline: none;
        }
        button {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            display: block;
            margin: 30px auto 0;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            display: none;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
        }
        .path-info {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        .save-info {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
            text-align: right;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>微信多开工具</h1>
        <form method="POST" action="/start">
            <div class="form-group">
                <label for="path">微信安装路径:</label>
                <input type="text" id="path" name="path" value="{{ default_path }}" placeholder="例如：C:\Program Files (x86)\Tencent\WeChat\WeChat.exe" required>
                <div class="path-info">如果自动检测的路径不正确，请手动输入正确的微信安装路径</div>
                <div class="save-info">路径会自动保存，下次启动时自动加载</div>
            </div>
            <div class="form-group">
                <label for="count">多开数量:</label>
                <input type="number" id="count" name="count" min="1" max="10" value="{{ default_count }}" required>
            </div>
            <button type="submit">启动微信</button>
        </form>
        <div id="status" class="status"></div>
    </div>
    <script>
        document.querySelector('form').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch('/start', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(data => {
                const status = document.getElementById('status');
                status.style.display = 'block';
                if (data.includes('成功')) {
                    status.className = 'status success';
                } else {
                    status.className = 'status error';
                }
                status.textContent = data;
            })
            .catch(error => {
                const status = document.getElementById('status');
                status.style.display = 'block';
                status.className = 'status error';
                status.textContent = '发生错误: ' + error;
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    config = load_config()
    default_path = get_default_wechat_path()
    return render_template_string(HTML_TEMPLATE, 
                                default_path=default_path,
                                default_count=config["count"])

@app.route('/start', methods=['POST'])
def start_wechat():
    # 获取微信路径
    wechat_path = request.form['path']
    if not wechat_path:
        return "请输入微信安装路径"
    
    # 获取多开数量
    try:
        count = int(request.form['count'])
        if count < 1 or count > 10:
            return "多开数量必须在1-10之间"
    except ValueError:
        return "请输入有效的多开数量"
    
    # 保存配置
    config = load_config()
    config["wechat_path"] = wechat_path
    config["count"] = count
    save_config(config)
    
    # 检查微信路径是否存在
    if not os.path.exists(wechat_path):
        return "微信路径不存在，请检查路径!"
    
    # 确保路径使用双反斜杠
    wechat_path = wechat_path.replace("\\", "\\\\")
    
    # 启动多个微信实例
    try:
        for _ in range(count):
            subprocess.Popen([wechat_path])
        return "微信已成功启动{}个实例!".format(count)
    except Exception as e:
        return "启动微信失败: {}".format(str(e))

def open_browser():
    """延迟1秒后打开浏览器"""
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == "__main__":
    # 创建线程来打开浏览器
    threading.Thread(target=open_browser).start()
    # 创建线程来运行系统托盘
    threading.Thread(target=setup_tray, daemon=True).start()
    # 启动Flask应用
    app.run(debug=False, host='127.0.0.1', port=5000)