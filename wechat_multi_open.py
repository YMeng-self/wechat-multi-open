import os
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk

class WeChatMultiOpenApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('微信多开工具')
        self.root.geometry('450x300')
        self.root.configure(bg='#f5f5f5')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Microsoft YaHei', 10), borderwidth=1, relief='solid', padding=5, bordercolor='#ddd', background='#4CAF50', foreground='white')
        style.configure('TEntry', font=('Microsoft YaHei', 10), padding=5)
        style.configure('TLabel', font=('Microsoft YaHei', 10), background='#f5f5f5')
        style.configure('TSpinbox', font=('Microsoft YaHei', 10))
        
        # 主框架
        self.main_frame = tk.Frame(self.root, padx=20, pady=20, bg='#f5f5f5', highlightbackground='#ddd', highlightthickness=1, bd=0)
        self.main_frame.pack(expand=True, fill='both')
        
        # 微信路径配置
        # 微信路径配置
        tk.Label(self.main_frame, text='微信路径:', font=('Microsoft YaHei', 10), bg='#f0f0f0').pack(anchor='w')
        path_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        path_frame.pack(fill='x', pady=5)
        
        self.path_input = tk.Entry(path_frame, width=40, font=('Microsoft YaHei', 10))
        self.path_input.insert(0, r"C:\\Program Files\\Tencent\\WeChat\\WeChat.exe")
        self.path_input.pack(side='left', padx=(0, 10))
        
        ttk.Button(path_frame, text='浏览...', command=self.browse_wechat_path, style='TButton').pack(side='left')
        
        # 多开数量配置
        tk.Label(self.main_frame, text='多开数量:', font=('Microsoft YaHei', 10), bg='#f0f0f0').pack(anchor='w', pady=(10, 0))
        self.count_spin = ttk.Spinbox(self.main_frame, from_=1, to=10, font=('Microsoft YaHei', 10))
        self.count_spin.set(2)
        self.count_spin.pack(anchor='w', pady=5)
        
        # 启动按钮
        ttk.Button(self.main_frame, text='启动微信', command=self.start_wechat, style='TButton').pack(pady=20, ipadx=20, ipady=5)
    
    def browse_wechat_path(self):
        path = filedialog.askopenfilename(initialdir=r"C:\\Program Files\\Tencent\\WeChat", 
                                        title='选择微信程序', 
                                        filetypes=[("Executable files", "*.exe")])
        if path:
            self.path_input.delete(0, tk.END)
            self.path_input.insert(0, path)
    
    def start_wechat(self):
        wechat_path = self.path_input.get()
        count = int(self.count_spin.get())
        
        if os.path.exists(wechat_path):
            for _ in range(count):
                subprocess.Popen([wechat_path])

if __name__ == "__main__":
    app = WeChatMultiOpenApp()
    app.root.mainloop()