import webview
import os
import subprocess
import sys
import json
import threading

from flask import Flask, render_template_string, request
from pystray import Icon, Menu, MenuItem
from PIL import Image


def resource_path(relative_path):
    """获取打包后资源的正确路径"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# falsk app
app = Flask(__name__)
app.template_folder = resource_path('data')  # 如果模板在data目录

# 配置文件路径
CONFIG_FILE = resource_path("data/wechat_config.json")

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


# 全局变量，用于控制托盘图标
tray_icon = None


# def on_window_closed(window):
#     """点击 X 按钮时隐藏窗口（而不是关闭）"""
#     window.hide()
#     return False  # 阻止默认关闭行为

def on_tray_click(icon, item, window):
    """点击托盘图标时恢复窗口"""
    window.show()
    window.restore()  # 如果窗口最小化，恢复它


def create_tray_icon(window):
    """创建系统托盘图标"""
    global tray_icon

    # 1. 加载图标（可以是 .ico 或 .png）
    try:
        image = Image.open(resource_path("data/wechat.ico"))
    except FileNotFoundError:
        # 创建默认图标
        from io import BytesIO
        img = Image.new('RGB', (64, 64), color='green')
        image = img

    # 2. 定义托盘菜单
    menu = Menu(
        MenuItem("显示", lambda: window.show()),
        MenuItem("隐藏", lambda: window.hide()),
        MenuItem("退出", lambda: (tray_icon.stop(), window.destroy())),
    )

    # 3. 创建托盘图标
    tray_icon = Icon("my_app", image, "我的应用", menu)
    tray_icon.run()


# 全局变量，HTML页面模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微信多开工具</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #07C160;
            --primary-dark: #06AD56;
            --secondary: #1989FA;
            --text: #333;
            --text-light: #666;
            --text-lighter: #999;
            --bg: #f8f8f8;
            --card-bg: #fff;
            --border: #eee;
            --success: #67C23A;
            --error: #F56C6C;
            --shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            --radius: 12px;
            --transition: all 0.3s ease;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            width: 100%;
            max-width: 480px;
            background: var(--card-bg);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 30px;
            position: relative;
            overflow: hidden;
        }

        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }

        h1 {
            text-align: center;
            margin-bottom: 24px;
            color: var(--text);
            font-weight: 700;
            font-size: 24px;
            position: relative;
            padding-bottom: 12px;
        }

        h1::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: var(--primary);
            border-radius: 3px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--text);
            font-size: 15px;
        }

        .input-wrapper {
            position: relative;
        }

        input[type="text"], 
        input[type="number"] {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            font-size: 15px;
            transition: var(--transition);
            background-color: var(--card-bg);
            color: var(--text);
        }

        input[type="text"]:focus, 
        input[type="number"]:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(7, 193, 96, 0.1);
            outline: none;
        }

        .helper-text {
            font-size: 13px;
            color: var(--text-lighter);
            margin-top: 6px;
            line-height: 1.4;
        }

        .save-info {
            font-size: 13px;
            color: var(--text-lighter);
            margin-top: 6px;
            text-align: right;
        }

        button {
            width: 100%;
            padding: 14px;
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: var(--radius);
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition);
            margin-top: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        button:hover {
            background-color: var(--primary-dark);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(7, 193, 96, 0.2);
        }

        button:active {
            transform: translateY(0);
        }

        .status {
            margin-top: 20px;
            padding: 14px;
            border-radius: var(--radius);
            text-align: center;
            font-size: 14px;
            display: none;
            animation: fadeIn 0.3s ease;
        }

        .success {
            background-color: rgba(103, 194, 58, 0.1);
            color: var(--success);
            border: 1px solid rgba(103, 194, 58, 0.3);
        }

        .error {
            background-color: rgba(245, 108, 108, 0.1);
            color: var(--error);
            border: 1px solid rgba(245, 108, 108, 0.3);
        }

        .logo {
            text-align: center;
            margin-bottom: 16px;
        }

        .logo img {
            height: 48px;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 480px) {
            .container {
                padding: 24px 20px;
            }
            
            h1 {
                font-size: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8.5 14.5C8.5 14.5 9.5 16 12 16C14.5 16 15.5 14.5 15.5 14.5M12 11H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#07C160" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <h1>微信多开工具</h1>
        <form method="POST" action="/start">
            <div class="form-group">
                <label for="path">微信安装路径</label>
                <div class="input-wrapper">
                    <input type="text" id="path" name="path" value="{{ default_path }}" placeholder="例如：C:\Program Files (x86)\Tencent\WeChat\WeChat.exe" required>
                </div>
                <div class="save-info">如果自动检测的路径不正确，请手动输入正确的微信安装路径</div>
                <div class="save-info">路径会自动保存，下次启动时自动加载</div>
            </div>
            <div class="form-group">
                <label for="count">多开数量</label>
                <div class="input-wrapper">
                    <input type="number" id="count" name="count" min="1" max="10" value="{{ default_count }}" required>
                </div>
            </div>
            <button type="submit">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                启动微信
            </button>
        </form>
        <div id="status" class="status"></div>
    </div>
    <script>
        document.querySelector('form').addEventListener('submit', function(e) {
            e.preventDefault();
            const button = this.querySelector('button');
            const originalText = button.innerHTML;
            button.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="animate-spin">
                <path d="M12 2V6M12 18V22M6 12H2M22 12H18M19.0784 19.0784L16.25 16.25M19.0784 4.99994L16.25 7.82837M4.92157 19.0784L7.75 16.25M4.92157 4.99994L7.75 7.82837" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg> 处理中...`;
            button.disabled = true;

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
                
                // 滚动到状态信息
                status.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            })
            .catch(error => {
                const status = document.getElementById('status');
                status.style.display = 'block';
                status.className = 'status error';
                status.textContent = '发生错误: ' + error.message;
            })
            .finally(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            });
        });

        // 添加旋转动画
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            .animate-spin {
                animation: spin 1s linear infinite;
            }
        `;
        document.head.appendChild(style);
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
        if count < 1 or count > 3:
            return "建议多开数量≤3"
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
            # 关键语句
            subprocess.Popen([wechat_path])
        return "微信已成功启动{}个实例!".format(count)
    except Exception as e:
        return "启动微信失败: {}".format(str(e))


def run_server():
    """运行WEB服务器"""
    app.run(debug=False, host='127.0.0.1', port=5000)


def create_window():
    """创建PyWebView窗口"""
    window = webview.create_window(
        # title='微信多开工具',
        title='',
        # url='http://127.0.0.1:5000/',
        url=app, 
        width=600,
        height=700,
        # icon='icon/wechat.ico',
        # gui='cef'
        resizable=True,
        confirm_close=False,
        # fullscreen=False,
        # local_api=True,
    )
    return window


def main():
    # 1. 创建 WebView 窗口
    window = create_window()

    # 2. 绑定窗口关闭事件（点击 X 时隐藏到托盘）
    # window.events.closed += lambda: on_window_closed(window)

    # 3. 在后台线程运行托盘图标
    tray_thread = threading.Thread(
        target=create_tray_icon,
        args=(window,),
        daemon=True,
    )
    tray_thread.start()

    # web_thread = threading.Thread(target=run_server, daemon=True)
    # web_thread.start()

    # 4. 启动 WebView
    webview.start()


if __name__ == "__main__":
    main()
    # t = threading.Thread(target=run_server, daemon=True)
    # t.start()
    # # 调用函数创建窗口，而不是直接调用 webview.start() 函数
    # window = create_window()  
    # webview.start(window, http_server=True, http_port=8080)
