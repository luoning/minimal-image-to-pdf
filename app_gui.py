import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import windnd
from core_service import convert_images_to_pdf

def get_resource_path(relative_path):
    """
    获取资源路径（用于 PyInstaller 打包后的临时资源释放路径）
    """
    try:
        # PyInstaller 在运行程序时会创建临时目录，并将路径存在 sys._MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MinimalConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF")
        self.root.geometry("380x150")
        self.root.resizable(False, False)
        
        # Apple 风格暗黑色系
        self.bg_color = "#121214"
        self.accent_color = "#a855f7"   # 紫色进度条
        self.text_color = "#e4e4e7"
        self.sub_text_color = "#71717a"
        
        self.root.configure(bg=self.bg_color)
        
        # 设置程序窗口框左上角的 Icon
        try:
            ico_path = get_resource_path("app.ico")
            if os.path.exists(ico_path):
                self.root.iconbitmap(ico_path)
        except Exception:
            pass
            
        self.is_processing = False
        self.selected_inputs = None
        self.auto_close_on_finish = False  # 转换完成后是否自动关闭软件
        
        self.setup_ui()
        self.setup_drag_drop()
        
        # 检测是否是通过直接拖拽文件/文件夹到 EXE 图标上启动
        if len(sys.argv) > 1:
            paths = [os.path.abspath(arg) for arg in sys.argv[1:] if not arg.startswith("-")]
            if paths:
                self.selected_inputs = paths
                self.auto_close_on_finish = True  # 拖拽到图标启动的，转换完自动关闭
                self.root.after(100, self.start_conversion)
        
    def setup_ui(self):
        # 创建整个窗口大小的可点击区域
        self.main_frame = tk.Frame(self.root, bg=self.bg_color, cursor="hand2")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.bind("<Button-1>", self.on_click_select)
        
        # 1. 拖入提示标签 (就绪态)
        self.tip_label = tk.Label(
            self.main_frame,
            text="拖入文件夹或多张图片",
            font=("Microsoft YaHei", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.tip_label.place(relx=0.5, rely=0.38, anchor="center")
        self.tip_label.bind("<Button-1>", self.on_click_select)
        
        self.sub_tip_label = tk.Label(
            self.main_frame,
            text="— 或点击此处手动选择 —",
            font=("Microsoft YaHei", 8),
            bg=self.bg_color,
            fg=self.sub_text_color
        )
        self.sub_tip_label.place(relx=0.5, rely=0.62, anchor="center")
        self.sub_tip_label.bind("<Button-1>", self.on_click_select)
        
        # 2. 进度条容器 (默认隐藏)
        self.progress_frame = tk.Frame(self.root, bg=self.bg_color)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="正在准备转换...",
            font=("Microsoft YaHei", 9),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.progress_label.pack(anchor="w", pady=5)
        
        # 进度条样式
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Minimal.Horizontal.TProgressbar",
            thickness=6,
            background=self.accent_color,
            troughcolor="#27272a",
            borderwidth=0
        )
        
        self.progress_val = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_val,
            maximum=100,
            style="Minimal.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
    def setup_drag_drop(self):
        windnd.hook_dropfiles(self.root, self.on_handle_drop)
        
    def on_handle_drop(self, files):
        if self.is_processing:
            return
        paths = []
        for f in files:
            try:
                paths.append(f.decode('utf-8'))
            except UnicodeDecodeError:
                paths.append(f.decode('gbk', errors='ignore'))
        self.selected_inputs = paths
        self.auto_close_on_finish = False  # 运行中拖拽的不自动关闭
        self.start_conversion()
        
    def on_click_select(self, event):
        if self.is_processing:
            return
        choice_win = tk.Toplevel(self.root)
        choice_win.title("选择输入源")
        choice_win.geometry("260x100")
        choice_win.resizable(False, False)
        choice_win.configure(bg=self.bg_color)
        choice_win.transient(self.root)
        choice_win.grab_set()
        
        # 居中窗口
        x = self.root.winfo_x() + 60
        y = self.root.winfo_y() + 25
        choice_win.geometry(f"+{x}+{y}")
        
        # 同时也把 icon 绑定到子窗口
        try:
            ico_path = get_resource_path("app.ico")
            if os.path.exists(ico_path):
                choice_win.iconbitmap(ico_path)
        except Exception:
            pass
            
        lbl = tk.Label(choice_win, text="您想要如何选择图片？", bg=self.bg_color, fg=self.text_color, font=("Microsoft YaHei", 9))
        lbl.pack(pady=12)
        
        btn_frame = tk.Frame(choice_win, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, padx=10)
        
        def choose_folder():
            choice_win.destroy()
            folder = filedialog.askdirectory()
            if folder:
                self.selected_inputs = [folder]
                self.auto_close_on_finish = False
                self.start_conversion()
                
        def choose_files():
            choice_win.destroy()
            file_types = [("图片文件", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif")]
            files = filedialog.askopenfilenames(filetypes=file_types)
            if files:
                self.selected_inputs = list(files)
                self.auto_close_on_finish = False
                self.start_conversion()
                
        tk.Button(btn_frame, text="选择文件夹", bg="#27272a", fg=self.text_color, bd=0, padx=10, pady=5, cursor="hand2", command=choose_folder).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text="选择多张图片", bg="#27272a", fg=self.text_color, bd=0, padx=10, pady=5, cursor="hand2", command=choose_files).pack(side=tk.RIGHT, padx=15)

    def start_conversion(self):
        if not self.selected_inputs or self.is_processing:
            return
        
        self.is_processing = True
        
        # 隐藏就绪态提示文字
        self.main_frame.pack_forget()
        
        # 展示进度条区域
        self.progress_frame.pack(fill=tk.X, padx=30, pady=40)
        self.progress_val.set(0)
        
        # 后台静默处理
        threading.Thread(target=self.run_conversion, daemon=True).start()
        
    def run_conversion(self):
        first_input = self.selected_inputs[0]
        if os.path.isdir(first_input):
            folder_name = os.path.basename(os.path.normpath(first_input)) or "output"
            parent_dir = os.path.dirname(os.path.normpath(first_input))
            output_pdf = os.path.join(parent_dir, f"{folder_name}.pdf")
        else:
            parent_dir = os.path.dirname(first_input)
            output_pdf = os.path.join(parent_dir, "combined.pdf")
            
        def progress_callback(current, total, filename):
            percent = (current / total) * 100
            self.progress_val.set(percent)
            display_name = filename if len(filename) <= 18 else filename[:15] + "..."
            self.progress_label.config(text=f"正在无损转换 ({int(percent)}%): {display_name}")
            self.root.update_idletasks()
            
        success = False
        try:
            convert_images_to_pdf(self.selected_inputs, output_pdf, progress_callback=progress_callback)
            success = True
            
            # 成功后在进度条上方显示绿色完成文字（不弹框）
            self.progress_label.config(text="✓ PDF 已成功生成！", fg="#10b981")
            self.progress_val.set(100)
            self.root.update_idletasks()
        except Exception as e:
            # 失败后显示红色错误信息（不弹框）
            self.progress_label.config(text=f"❌ 错误: {e}", fg="#ef4444")
            self.root.update_idletasks()
        finally:
            self.is_processing = False
            
            if success:
                if self.auto_close_on_finish:
                    # 拖入到图标启动转换成功的，停留 1.5 秒展示“完成”状态后自动退出程序
                    self.root.after(1500, self.root.destroy)
                else:
                    # 窗口中操作转换成功的，停留 3 秒展示成果，然后静默重置回默认就绪状态
                    self.root.after(3000, self.reset_to_default)
            else:
                # 转换失败的，停留 6 秒让用户看清错误原因，然后恢复默认就绪状态
                self.root.after(6000, self.reset_to_default)

    def reset_to_default(self):
        if self.is_processing:
            return
        # 恢复文字颜色和进度条隐藏，还原初始界面
        self.progress_label.config(text="正在准备转换...", fg=self.text_color)
        self.progress_frame.pack_forget()
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.selected_inputs = None

if __name__ == "__main__":
    # 启用高 DPI 适配
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
        
    root = tk.Tk()
    app = MinimalConverterApp(root)
    root.mainloop()
