import os
import sys
import argparse
from core_service import convert_images_to_pdf

def print_progress(current, total, filename):
    """
    在终端绘制设计精美的进度条
    """
    percent = (current / total) * 100
    bar_width = 30
    # 使用中英文通用的字符绘制高对比度进度条
    filled_length = int(round(bar_width * current / float(total)))
    bar = '█' * filled_length + '░' * (bar_width - filled_length)
    
    # 截断文件名，防止终端折行
    display_name = filename
    if len(filename) > 22:
        display_name = filename[:19] + "..."
        
    # \r 使光标回到行首，实现原地更新
    sys.stdout.write(f"\r  [*] 进度: [{bar}] {percent:5.1f}% ({current}/{total}) | 正在处理: {display_name:<22}")
    sys.stdout.flush()

def main():
    # 检测是否为拖拽路径启动 (不以 - 开头，且 argv 长度大于 1)
    use_drag_drop = False
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        use_drag_drop = True
        
    if use_drag_drop:
        # 获取所有被拖拽的文件/文件夹绝对路径
        inputs = [os.path.abspath(arg) for arg in sys.argv[1:]]
        
        first_input = inputs[0]
        if os.path.isdir(first_input):
            folder_name = os.path.basename(os.path.normpath(first_input)) or "output"
            parent_dir = os.path.dirname(os.path.normpath(first_input))
            output_pdf = os.path.join(parent_dir, f"{folder_name}.pdf")
        else:
            parent_dir = os.path.dirname(first_input)
            output_pdf = os.path.join(parent_dir, "combined.pdf")
            
        folder_log_name = f"拖拽的文件/文件夹列表 ({len(inputs)} 个对象)"
    else:
        # 使用普通的命令行参数解析
        parser = argparse.ArgumentParser(
            description="PDF 无损合并与压缩 CLI 服务",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "-f", "--folder", 
            type=str, 
            default="",
            help="待处理的图片文件夹路径"
        )
        parser.add_argument(
            "-o", "--output", 
            type=str, 
            default=None,
            help="输出的 PDF 文件路径"
        )
        
        args = parser.parse_args()
        
        folder_arg = args.folder.strip()
        if not folder_arg:
            print("=" * 60)
            print("  PDF 无损合成与压缩服务 (CLI/拖拽版)")
            print("=" * 60)
            print("[提示] 您可以直接把图片文件夹或多张图片拖拽到本程序图标上进行快速转换。")
            print("-" * 60)
            
            user_input = input("请输入或粘贴图片文件夹路径 (或拖入文件夹): ").strip()
            user_input = user_input.replace('"', '').replace("'", "")
            
            if not user_input:
                print("[-] 错误: 未输入任何路径，程序退出。", file=sys.stderr)
                input("\n按回车键退出...")
                sys.exit(1)
            folder_path = os.path.abspath(user_input)
        else:
            folder_path = os.path.abspath(folder_arg)
            
        inputs = folder_path
        folder_log_name = folder_path
        
        if args.output:
            output_pdf = os.path.abspath(args.output)
        else:
            folder_name = os.path.basename(os.path.normpath(folder_path)) or "output"
            parent_dir = os.path.dirname(os.path.normpath(folder_path))
            output_pdf = os.path.join(parent_dir, f"{folder_name}.pdf")
            
    # 执行业务逻辑前界面渲染
    if not use_drag_drop and folder_arg:
        print("=" * 60)
        print("  PDF 无损合成与压缩服务 (CLI 版)")
        print("=" * 60)
    elif use_drag_drop:
        print("=" * 60)
        print("  PDF 无损合成与压缩服务 (拖拽处理)")
        print("=" * 60)
        
    print(f"[*] 输入来源: {folder_log_name}")
    print(f"[*] 输出路径: {output_pdf}")
    print("[*] 正在进行视觉无损压缩并打包为 A4 PDF...")
    print("-" * 60)
    
    try:
        # 传入进度回调函数
        sorted_images = convert_images_to_pdf(inputs, output_pdf, progress_callback=print_progress)
        
        # 换行，防止最后的成功输出贴在进度条后面
        print()
        pdf_size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
        print("-" * 60)
        print(f"[+] 合成完成! PDF 文件已成功生成。")
        print(f"[+] 转换统计: 共处理 {len(sorted_images)} 张图片")
        print(f"[+] 页面规格: A4 页面 (强制纵向排版，横向图缩放居中)")
        print(f"[+] PDF 大小: {pdf_size_mb:.2f} MB (视觉无损压缩)")
        print(f"[+] PDF 位置: {output_pdf}")
        print("=" * 60)
        
    except Exception as e:
        print()
        print(f"[-] 错误: 处理失败: {e}", file=sys.stderr)
        if len(sys.argv) == 1 or use_drag_drop:
            input("\n按回车键退出...")
        sys.exit(1)
        
    if len(sys.argv) == 1 or use_drag_drop:
        input("\n处理完成！按回车键退出...")

if __name__ == "__main__":
    main()
