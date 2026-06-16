# ImageToPDF 极简无损图片转 PDF 工具

[![GitHub Release](https://img.shields.io/github/v/release/luoning/ImageToPDF?color=purple&logo=github)](https://github.com/luoning/ImageToPDF/releases)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

一款遵循极简主义设计理念的绿色免安装图片转 PDF 桌面小工具。专为将零散图片（如手机扫描件、文档照片等）快速合并、无损压缩打包为标准 A4 规格的 PDF 文件而设计。

---

## 🎨 极简交互设计

- **零多余点击**：直接将图片或文件夹拖入 `ImageToPDF.exe` 图标上，即刻自动开始转换，没有任何弹窗，转换完成后自动退出。
- **极小视觉干扰**：运行窗口仅 380x150 像素。界面中央只展示高对比度的紫色动态进度条，无杂乱按钮。
- **静默成功机制**：转换成功时，界面显示 `✓ PDF 已成功生成！`，停留 1.5 秒后自动关闭。

---

## ✨ 核心功能

1. **视觉无损压缩**：自动对图片进行高质量 JPEG 重编码，在肉眼完全无法察觉画质差异的前提下，**将 PDF 体积缩减约 90%**（例如：82MB 原始图片集打包后 PDF 仅为 8.9MB），极大提升传输效率。
2. **强制纵向 A4 排版**：每张图片独占一页 A4 页面（宽 210mm x 高 297mm），图片自动缩放居中展示，横版图片保持纵向布局上下留白，**绝不拉伸变形**。
3. **自然数值排序**：自动按照文件名数值顺序排列（例如：`1.jpg`, `2.jpg`, `10.jpg`, `11.jpg`），避免 ASCII 字典序导致的排序错乱。
4. **EXIF 方向修正**：内置 EXIF 属性读取，自动根据拍照角度扶正页面，转换出来的 PDF 页面绝对不会上下颠倒。
5. **多端拖拽支持**：支持直接拖拽单个/多个文件夹、多张图片混合拖入到图标或运行中的窗口中。

---

## 🚀 如何使用它？

### 方式一：拖拽一键合成（极力推荐）
- **操作**：选中需要打包的文件夹，或按住 `Ctrl` 键多选多张图片，直接**拖拽并释放在 `ImageToPDF.exe` 图标上**。
- **效果**：程序会自动在同级目录下无损生成对应的 PDF 并显示进度条，完成后自动退出。

### 方式二：双击选择运行
- **操作**：直接双击运行 `ImageToPDF.exe`，点击窗口任意区域。
- **效果**：会弹出选择菜单，您可以分别手动选择“整个文件夹”或“选择多张图片”进行转换。

---

## 🛠️ 本地开发与从源码运行

如果您想修改代码或在本地运行：

1. **克隆仓库**：
   ```bash
   git clone https://github.com/luoning/ImageToPDF.git
   cd ImageToPDF
   ```
2. **创建并激活虚拟环境**：
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   ```
3. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```
4. **运行程序**：
   ```bash
   python app_gui.py
   ```
5. **本地编译打包**：
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --noconsole --name="ImageToPDF" --icon=app.ico --add-data "app.ico;." app_gui.py
   ```

---

## 📦 项目结构

```text
├── .gitignore
├── app_gui.py        # 极简 GUI 界面主程序
├── core_service.py   # 图片压缩、纠偏及 PDF 封装核心逻辑
├── app.ico           # 去除白底、满格裁剪的专属精美 Icon 图标
├── README.md         # 项目说明文档
└── requirements.txt  # 运行依赖项
```

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。
