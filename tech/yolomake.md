# 图像批量旋转与YOLO标注工具说明

## 源代码

### image_rotator.py
```python
```

### yolo_visuailizer.py
```python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import sys
import glob

# 设置标准输出编码为UTF-8以支持中文显示
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

class YOLOVisualizer:
    def __init__(self):
        self.colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    
    def draw_yolo_bbox(self, image, yolo_label, class_id=0, confidence=1.0):
        """在图像上绘制YOLO格式的边界框"""
        height, width = image.shape[:2]
        center_x, center_y, bbox_width, bbox_height = yolo_label
        
        # 转换为像素坐标
        pixel_center_x = int(center_x * width)
        pixel_center_y = int(center_y * height)
        pixel_width = int(bbox_width * width)
        pixel_height = int(bbox_height * height)
        
        # 计算边界框的左上角和右下角
        x1 = int(pixel_center_x - pixel_width / 2)
        y1 = int(pixel_center_y - pixel_height / 2)
        x2 = int(pixel_center_x + pixel_width / 2)
        y2 = int(pixel_center_y + pixel_height / 2)
        
        # 选择颜色
        color = self.colors[class_id % len(self.colors)]
        
        # 绘制边界框
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        
        # 添加标签
        label = f"Class {class_id}: {confidence:.2f}"
        cv2.putText(image, label, (x1, y1 - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return image
    
    def load_yolo_labels(self, label_path):
        """加载YOLO格式的标签文件"""
        labels = []
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        class_id = int(parts[0])
                        center_x = float(parts[1])
                        center_y = float(parts[2])
                        bbox_width = float(parts[3])
                        bbox_height = float(parts[4])
                        confidence = float(parts[5]) if len(parts) > 5 else 1.0
                        labels.append((class_id, center_x, center_y, bbox_width, bbox_height, confidence))
        return labels
    
    def visualize_image_with_labels(self, image_path, label_path=None):
        """可视化图像和对应的标签"""
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法加载图像: {image_path}")
            return None
        
        # 如果没有指定标签路径，尝试自动查找
        if label_path is None:
            base_name = os.path.splitext(image_path)[0]
            label_path = base_name + '.txt'
        
        # 加载标签
        labels = self.load_yolo_labels(label_path)
        
        # 在图像上绘制所有边界框
        for label in labels:
            class_id, center_x, center_y, bbox_width, bbox_height, confidence = label
            image = self.draw_yolo_bbox(image, (center_x, center_y, bbox_width, bbox_height), class_id, confidence)
        
        return image
    
    def show_rotated_images(self, rotation_folder, max_images=20, step=15):
        """显示旋转后的图像和标签"""
        # 查找所有图像文件
        image_files = glob.glob(os.path.join(rotation_folder, "*.jpg"))
        image_files.sort()
        
        if not image_files:
            print(f"在文件夹 {rotation_folder} 中未找到图像文件")
            return
        
        # 如果图像数量很多，按步长采样显示
        if len(image_files) > max_images:
            sampled_files = image_files[::step][:max_images]
            print(f"图像数量较多({len(image_files)}个)，按步长{step}采样显示 {len(sampled_files)} 个图像...")
        else:
            sampled_files = image_files[:max_images]
            print(f"显示 {len(sampled_files)} 个旋转图像...")
        
        for i, image_path in enumerate(sampled_files):
            # 可视化图像和标签
            visualized = self.visualize_image_with_labels(image_path)
            
            if visualized is not None:
                # 调整图像大小以适应显示
                height, width = visualized.shape[:2]
                max_size = 600
                if max(height, width) > max_size:
                    scale = max_size / max(height, width)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    visualized = cv2.resize(visualized, (new_width, new_height))
                
                # 显示图像
                filename = os.path.basename(image_path)
                cv2.imshow(f"旋转结果: {filename}", visualized)
                
                print(f"显示: {filename} ({i+1}/{len(sampled_files)}) (按任意键继续，ESC退出)")
                key = cv2.waitKey(0) & 0xFF
                cv2.destroyAllWindows()
                
                if key == 27:  # ESC键退出
                    break
    
    def show_specific_angles(self, rotation_folder, angles=[0, 90, 180, 270]):
        """显示特定角度的旋转图像"""
        print(f"显示特定角度的旋转图像: {angles}")
        
        for angle in angles:
            # 查找特定角度的图像
            angle_pattern = os.path.join(rotation_folder, f"*_{angle:03d}deg.jpg")
            angle_files = glob.glob(angle_pattern)
            
            if angle_files:
                image_path = angle_files[0]
                visualized = self.visualize_image_with_labels(image_path)
                
                if visualized is not None:
                    # 调整图像大小以适应显示
                    height, width = visualized.shape[:2]
                    max_size = 600
                    if max(height, width) > max_size:
                        scale = max_size / max(height, width)
                        new_width = int(width * scale)
                        new_height = int(height * scale)
                        visualized = cv2.resize(visualized, (new_width, new_height))
                    
                    # 显示图像
                    filename = os.path.basename(image_path)
                    cv2.imshow(f"旋转结果: {filename}", visualized)
                    
                    print(f"显示: {filename} (按任意键继续，ESC退出)")
                    key = cv2.waitKey(0) & 0xFF
                    cv2.destroyAllWindows()
                    
                    if key == 27:  # ESC键退出
                        break
            else:
                print(f"未找到角度为 {angle}° 的图像文件")

def main():
    visualizer = YOLOVisualizer()
    
    print("=== YOLO标签可视化工具 ===")
    print("此工具可以帮助您查看旋转后的图像和对应的YOLO标签")
    print()
    
    # 查找所有旋转文件夹
    rotation_folders = glob.glob("images/*_rotations")
    
    if not rotation_folders:
        print("未找到任何旋转结果文件夹")
        print("请先运行 image_rotator.py 来生成旋转图像")
        return
    
    print(f"找到 {len(rotation_folders)} 个旋转文件夹:")
    for i, folder in enumerate(rotation_folders):
        # 统计每个文件夹中的图像数量
        image_count = len(glob.glob(os.path.join(folder, "*.jpg")))
        print(f"{i+1}. {folder} ({image_count} 个图像)")
    
    # 让用户选择要查看的文件夹
    choice = input(f"请选择要查看的文件夹 (1-{len(rotation_folders)}): ").strip()
    
    try:
        folder_index = int(choice) - 1
        if 0 <= folder_index < len(rotation_folders):
            selected_folder = rotation_folders[folder_index]
            print(f"正在查看文件夹: {selected_folder}")
            
            # 选择查看模式
            print("\n选择查看模式:")
            print("1. 查看特定角度 (0°, 90°, 180°, 270°)")
            print("2. 采样查看 (每15度一个)")
            print("3. 查看前20个")
            print("4. 自定义角度")
            
            view_choice = input("请输入选择 (1-4): ").strip()
            
            if view_choice == "1":
                visualizer.show_specific_angles(selected_folder)
            elif view_choice == "2":
                visualizer.show_rotated_images(selected_folder, max_images=24, step=15)
            elif view_choice == "3":
                visualizer.show_rotated_images(selected_folder, max_images=20, step=1)
            elif view_choice == "4":
                angles_input = input("请输入要查看的角度（用逗号分隔，如: 0,45,90,135,180）: ").strip()
                try:
                    angles = [int(x.strip()) for x in angles_input.split(',')]
                    visualizer.show_specific_angles(selected_folder, angles)
                except ValueError:
                    print("输入格式错误")
            else:
                print("无效选择")
                
        else:
            print("无效选择")
    except ValueError:
        print("请输入有效的数字")

if __name__ == "__main__":
    main()

```

## 功能描述
本工具可对 images 文件夹下所有 jpg 图像进行批量旋转（360次，每次1°），并为每张图像手动打标，自动生成YOLO格式标签，类别ID从0递增。支持旋转后标签同步变换。可配合 yolo_visualizer.py 可视化旋转结果。

## 使用方法

### 1. 图像批量旋转与标注
- 将所有待处理的 jpg 图像放入 images 文件夹。
- 运行：
```bash
python image_rotator.py
```
- 选择“1. 直接开始旋转所有图像（包括标签选择）”。
- 按提示为每张图像用鼠标点击两个对角点，定义目标物体的边界框。
- 每张图像会自动分配一个类别ID（从0递增）。
- 工具会自动对每张图像生成360个旋转版本及对应标签。

### 2. 可视化旋转结果
- 运行：
```bash
python yolo_visualizer.py
```
- 选择旋转结果文件夹，可按角度采样或自定义角度查看旋转效果和标签。

## 输出文件结构
```
images/
├── image1.jpg                    # 原始图像1 (类别ID: 0)
├── image1.txt                    # 原始YOLO标签1
├── image1_rotations/             # 旋转结果文件夹1
│   ├── image1_000deg.jpg         # 旋转0°图像
│   ├── image1_000deg.txt         # 旋转0°标签 (类别ID: 0)
│   ├── image1_001deg.jpg         # 旋转1°图像
│   ├── image1_001deg.txt         # 旋转1°标签 (类别ID: 0)
│   └── ...                       # 其他旋转角度
├── image2.jpg                    # 原始图像2 (类别ID: 1)
├── image2.txt                    # 原始YOLO标签2
├── image2_rotations/             # 旋转结果文件夹2
│   ├── image2_000deg.jpg         # 旋转0°图像
│   ├── image2_000deg.txt         # 旋转0°标签 (类别ID: 1)
│   └── ...                       # 其他旋转角度
└── ...                           # 其他图像和文件夹
```

## YOLO标签格式
每个标签文件一行：
```
class_id center_x center_y width height
```
- class_id：类别ID（从0递增）
- center_x, center_y, width, height：均为归一化（0-1）

## 注意事项
- 每张图像会生成360个旋转版本，请确保磁盘空间充足。
- 类别ID自动分配，顺序与images文件夹下jpg文件顺序一致。
- 标注时请确保框选完整目标。
- 支持任意jpg图片批量处理。

## 依赖
- Python 3.x
- opencv-python
- numpy

## 示例流程
1. 将图片放入 images/
2. 运行 python image_rotator.py，依次打标
3. 运行 python yolo_visualizer.py 检查旋转与标签效果
