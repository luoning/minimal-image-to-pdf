import os
import shutil
import tempfile
from PIL import Image, ImageOps
import img2pdf
from natsort import natsorted

SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

def convert_images_to_pdf(inputs, output_pdf_path, quality=80, progress_callback=None):
    """
    将输入的图片文件或文件夹中的图片合并输出为 A4 纵向 PDF，并进行视觉无损压缩（Quality=80）
    
    :param inputs: 可以是文件夹路径(str)，也可以是图片文件路径列表(list)
    :param output_pdf_path: 输出的 PDF 文件绝对路径
    :param quality: JPEG 压缩质量（默认 80）
    :param progress_callback: 进度回调函数，格式为 callback(current_index, total_count, current_filename)
    """
    image_files = []
    
    # 1. 解析输入源
    if isinstance(inputs, str):
        if not os.path.exists(inputs):
            raise ValueError(f"路径不存在: {inputs}")
        if os.path.isdir(inputs):
            all_files = os.listdir(inputs)
            for file in all_files:
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_FORMATS:
                    image_files.append(os.path.join(inputs, file))
        else:
            ext = os.path.splitext(inputs)[1].lower()
            if ext in SUPPORTED_FORMATS:
                image_files.append(inputs)
    elif isinstance(inputs, list):
        for item in inputs:
            if os.path.isdir(item):
                for file in os.listdir(item):
                    ext = os.path.splitext(file)[1].lower()
                    if ext in SUPPORTED_FORMATS:
                        image_files.append(os.path.join(item, file))
            elif os.path.isfile(item):
                ext = os.path.splitext(item)[1].lower()
                if ext in SUPPORTED_FORMATS:
                    image_files.append(item)
                    
    if not image_files:
        raise ValueError("未找到任何支持的图片文件")
    
    # 2. 自然排序
    sorted_images = natsorted(image_files)
    total_images = len(sorted_images)
    
    # 3. 创建临时文件夹存放压缩后的图片
    temp_dir = tempfile.mkdtemp()
    compressed_images = []
    
    try:
        for idx, img_path in enumerate(sorted_images, 1):
            filename = os.path.basename(img_path)
            # 触发进度回调 (处理前)
            if progress_callback:
                progress_callback(idx, total_images, filename)
                
            temp_img_path = os.path.join(temp_dir, f"{idx:05d}.jpg")
            
            with Image.open(img_path) as img:
                # 自动处理 EXIF 旋转属性
                img = ImageOps.exif_transpose(img)
                
                # 如果是 RGBA 或 P 模式，转换为 RGB
                if img.mode in ('RGBA', 'LA', 'P'):
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        bg.paste(img, mask=img.split()[3])
                    else:
                        bg.paste(img)
                    img = bg
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 视觉无损压缩保存为 JPEG
                img.save(temp_img_path, 'JPEG', optimize=True, quality=quality)
                
            compressed_images.append(temp_img_path)
            
        # 设置 A4 纸张大小
        a4_width = img2pdf.mm_to_pt(210)
        a4_height = img2pdf.mm_to_pt(297)
        
        # 使用 img2pdf 布局函数
        layout_fun = img2pdf.get_layout_fun(
            pagesize=(a4_width, a4_height),
            fit=img2pdf.FitMode.into,
            auto_orient=False
        )
        
        # 写入 PDF
        with open(output_pdf_path, 'wb') as f:
            f.write(img2pdf.convert(compressed_images, layout_fun=layout_fun))
            
    finally:
        # 清理所有临时文件和文件夹
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass
            
    return sorted_images
