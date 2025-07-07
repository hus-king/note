# 图像批量旋转与YOLO标注工具说明

## 源代码

### image_rotator.py
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
    # 设置环境变量以支持中文
    os.environ['PYTHONIOENCODING'] = 'utf-8'

class ImageRotator:
    def __init__(self):
        self.rotation_step = 1  # 每次旋转1度
        self.total_rotations = 360  # 总共旋转360次
        self.points = []
        self.image = None
        self.window_name = ""
        self.yolo_label = None
        
    def mouse_callback(self, event, x, y, flags, param):
        """鼠标回调函数，用于选择两个点"""
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.points) < 2:
                self.points.append((x, y))
                print(f"选择了点: ({x}, {y})")
                
                # 在图像上绘制选择的点
                cv2.circle(self.image, (x, y), 5, (0, 255, 0), -1)
                cv2.imshow(self.window_name, self.image)
                
                if len(self.points) == 2:
                    # 绘制矩形框
                    cv2.rectangle(self.image, self.points[0], self.points[1], (0, 255, 0), 2)
                    cv2.imshow(self.window_name, self.image)
                    print("已选择两个点，按任意键继续...")
    
    def select_bounding_box(self, image_path):
        """选择边界框并转换为YOLO格式"""
        self.points = []
        self.image = cv2.imread(image_path)
        if self.image is None:
            print(f"无法加载图像: {image_path}")
            return None
            
        self.window_name = "选择边界框 - 点击两个对角点"
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        
        print(f"请在图像中选择两个点来定义边界框")
        cv2.imshow(self.window_name, self.image)
        
        # 等待用户选择两个点
        while len(self.points) < 2:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC键退出
                cv2.destroyAllWindows()
                return None
        
        # 等待用户按键确认
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # 获取图像尺寸
        height, width = self.image.shape[:2]
        
        # 计算边界框坐标
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        
        # 确保坐标正确（左上角和右下角）
        x_min = min(x1, x2)
        y_min = min(y1, y2)
        x_max = max(x1, x2)
        y_max = max(y1, y2)
        
        # 转换为YOLO格式 (归一化的中心点坐标和宽高)
        center_x = (x_min + x_max) / 2.0 / width
        center_y = (y_min + y_max) / 2.0 / height
        bbox_width = (x_max - x_min) / width
        bbox_height = (y_max - y_min) / height
        
        self.yolo_label = (center_x, center_y, bbox_width, bbox_height)
        
        print(f"边界框坐标: ({x_min}, {y_min}, {x_max}, {y_max})")
        print(f"YOLO格式: {center_x:.6f} {center_y:.6f} {bbox_width:.6f} {bbox_height:.6f}")
        
        return self.yolo_label
    
    def rotate_yolo_bbox(self, yolo_label, angle, original_width, original_height, new_width, new_height):
        """旋转YOLO格式的边界框"""
        center_x, center_y, bbox_width, bbox_height = yolo_label
        
        # 转换为像素坐标
        pixel_center_x = center_x * original_width
        pixel_center_y = center_y * original_height
        pixel_width = bbox_width * original_width
        pixel_height = bbox_height * original_height
        
        # 计算边界框的四个角点
        half_width = pixel_width / 2
        half_height = pixel_height / 2
        
        corners = [
            (pixel_center_x - half_width, pixel_center_y - half_height),  # 左上
            (pixel_center_x + half_width, pixel_center_y - half_height),  # 右上
            (pixel_center_x + half_width, pixel_center_y + half_height),  # 右下
            (pixel_center_x - half_width, pixel_center_y + half_height)   # 左下
        ]
        
        # 旋转矩阵
        angle_rad = np.radians(angle)
        cos_angle = np.cos(angle_rad)
        sin_angle = np.sin(angle_rad)
        
        # 原图像中心点
        orig_center_x = original_width / 2
        orig_center_y = original_height / 2
        
        # 旋转后的中心点偏移
        new_center_x = new_width / 2
        new_center_y = new_height / 2
        
        # 旋转所有角点
        rotated_corners = []
        for x, y in corners:
            # 相对于原图像中心的坐标
            rel_x = x - orig_center_x
            rel_y = y - orig_center_y
            
            # 旋转
            new_x = rel_x * cos_angle - rel_y * sin_angle
            new_y = rel_x * sin_angle + rel_y * cos_angle
            
            # 转换到新图像坐标系
            final_x = new_x + new_center_x
            final_y = new_y + new_center_y
            
            rotated_corners.append((final_x, final_y))
        
        # 计算旋转后的边界框
        x_coords = [corner[0] for corner in rotated_corners]
        y_coords = [corner[1] for corner in rotated_corners]
        
        x_min = max(0, min(x_coords))
        y_min = max(0, min(y_coords))
        x_max = min(new_width, max(x_coords))
        y_max = min(new_height, max(y_coords))
        
        # 转换为YOLO格式
        new_center_x = (x_min + x_max) / 2.0 / new_width
        new_center_y = (y_min + y_max) / 2.0 / new_height
        new_bbox_width = (x_max - x_min) / new_width
        new_bbox_height = (y_max - y_min) / new_height
        
        return (new_center_x, new_center_y, new_bbox_width, new_bbox_height)
    
    def save_yolo_label(self, label_path, yolo_label, class_id=0):
        """保存YOLO格式的标签文件"""
        with open(label_path, 'w') as f:
            center_x, center_y, bbox_width, bbox_height = yolo_label
            f.write(f"{class_id} {center_x:.6f} {center_y:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")
    
    def save_classes_file(self, images_folder, class_names):
        """保存classes.txt文件"""
        classes_path = os.path.join(images_folder, "classes.txt")
        with open(classes_path, 'w', encoding='utf-8') as f:
            for class_name in class_names:
                f.write(f"{class_name}\n")
        print(f"类别文件已保存到: {classes_path}")
        return classes_path
    
    def rotate_image(self, image, angle):
        """
        旋转图像指定角度
        """
        # 获取图像尺寸
        height, width = image.shape[:2]
        
        # 计算旋转中心点
        center = (width // 2, height // 2)
        
        # 创建旋转矩阵
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # 计算旋转后的图像尺寸
        cos_angle = abs(rotation_matrix[0, 0])
        sin_angle = abs(rotation_matrix[0, 1])
        
        new_width = int((height * sin_angle) + (width * cos_angle))
        new_height = int((height * cos_angle) + (width * sin_angle))
        
        # 调整旋转矩阵以适应新的图像尺寸
        rotation_matrix[0, 2] += (new_width / 2) - center[0]
        rotation_matrix[1, 2] += (new_height / 2) - center[1]
        
        # 执行旋转
        rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height), 
                                     borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
        
        return rotated_image, new_width, new_height
    
    def process_all_images(self, images_folder="images"):
        """
        处理images文件夹中的所有jpg图像文件
        """
        # 查找所有jpg图像文件
        jpg_pattern = os.path.join(images_folder, "*.jpg")
        all_images = glob.glob(jpg_pattern)
        
        # 过滤掉旋转生成的图像（包含deg的文件名）
        original_images = [img for img in all_images if 'deg.jpg' not in img]
        
        if not original_images:
            print("未找到任何jpg图像文件")
            return
        
        print(f"找到 {len(original_images)} 个原始图像文件:")
        for img in original_images:
            print(f"  - {img}")
        
        # 收集类别名称
        class_names = []
        current_class_id = 0  # YOLO标签类别从0开始
        
        for image_path in original_images:
            print(f"\n正在处理: {image_path}")
            print(f"当前类别ID: {current_class_id}")
            
            # 询问类别名称
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            default_class_name = base_name  # 使用文件名作为默认类别名
            class_name = default_class_name
            class_names.append(class_name)
            
            # 为每个图像选择边界框
            print(f"请为图像 {image_path} 选择边界框")
            yolo_label = self.select_bounding_box(image_path)
            
            if yolo_label is None:
                print(f"跳过图像 {image_path}")
                continue
                
            # 保存原始标签
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            original_label_path = os.path.join(images_folder, f"{base_name}.txt")
            self.save_yolo_label(original_label_path, yolo_label, current_class_id)
            print(f"原始标签已保存到: {original_label_path} (类别ID: {current_class_id}, 类别名: {class_name})")
            
            # 旋转图像和标签
            self.rotate_single_image(image_path, yolo_label, current_class_id)
            
            # 类别ID递增
            current_class_id += 1
        
        # 保存classes.txt文件
        if class_names:
            self.save_classes_file(images_folder, class_names)
            print(f"\n处理完成！共处理 {len(class_names)} 个类别：")
            for i, name in enumerate(class_names):
                print(f"  {i}: {name}")
    
    def rotate_single_image(self, image_path, yolo_label, class_id=0):
        """
        旋转单个图像360次，每次旋转1度，同时生成对应的标签
        """
        # 加载图像
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法加载图像: {image_path}")
            return
        
        original_height, original_width = image.shape[:2]
        
        # 获取文件名和路径信息
        image_dir = os.path.dirname(image_path)
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        
        # 创建旋转图像文件夹
        rotation_folder = os.path.join(image_dir, f"{image_name}_rotations")
        if not os.path.exists(rotation_folder):
            os.makedirs(rotation_folder)
        
        print(f"开始旋转 {image_name}... (类别ID: {class_id})")
        
        # 进行360次旋转
        for i in range(self.total_rotations):
            angle = i * self.rotation_step
            
            # 旋转图像
            rotated_image, new_width, new_height = self.rotate_image(image, angle)
            
            # 旋转标签
            rotated_label = self.rotate_yolo_bbox(yolo_label, angle, original_width, original_height, new_width, new_height)
            
            # 保存旋转后的图像
            output_filename = f"{image_name}_{angle:03d}deg.jpg"
            output_path = os.path.join(rotation_folder, output_filename)
            cv2.imwrite(output_path, rotated_image)
            
            # 保存旋转后的标签，使用传入的class_id
            label_filename = f"{image_name}_{angle:03d}deg.txt"
            label_path = os.path.join(rotation_folder, label_filename)
            self.save_yolo_label(label_path, rotated_label, class_id)
            
            # 每10度显示一次进度
            if angle % 10 == 0:
                print(f"已保存: {output_filename} 和 {label_filename} (旋转 {angle}°, 类别ID: {class_id})")
        
        print(f"完成! 所有旋转图像和标签已保存到: {rotation_folder}")
        print(f"共生成 {self.total_rotations} 个旋转图像和标签文件 (类别ID: {class_id})")
    
    def create_rotation_preview(self, image_path, preview_angles=[0, 90, 180, 270]):
        """
        创建旋转预览图，显示指定角度的旋转效果
        """
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法加载图像: {image_path}")
            return
        
        # 调整图像大小以适应预览
        height, width = image.shape[:2]
        max_size = 200
        if max(height, width) > max_size:
            scale = max_size / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height))
        
        # 创建预览图像
        preview_images = []
        max_height = 0
        max_width = 0
        
        # 先生成所有旋转图像，并记录最大尺寸
        for angle in preview_angles:
            rotated, rot_width, rot_height = self.rotate_image(image, angle)
            # 添加角度标签
            cv2.putText(rotated, f"{angle}deg", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            preview_images.append(rotated)
            
            # 记录最大尺寸
            max_height = max(max_height, rot_height)
            max_width = max(max_width, rot_width)
        
        # 将所有预览图像调整为相同尺寸
        normalized_images = []
        for img in preview_images:
            # 创建白色背景
            normalized = np.ones((max_height, max_width, 3), dtype=np.uint8) * 255
            
            # 计算居中位置
            h, w = img.shape[:2]
            y_offset = (max_height - h) // 2
            x_offset = (max_width - w) // 2
            
            # 将图像放置在中心
            normalized[y_offset:y_offset+h, x_offset:x_offset+w] = img
            normalized_images.append(normalized)
        
        # 将预览图像合并为一个大图
        if len(normalized_images) >= 4:
            top_row = np.hstack([normalized_images[0], normalized_images[1]])
            bottom_row = np.hstack([normalized_images[2], normalized_images[3]])
            combined = np.vstack([top_row, bottom_row])
        else:
            combined = np.hstack(normalized_images)
        
        # 显示预览
        cv2.imshow("旋转预览", combined)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    rotator = ImageRotator()
    
    print("=== 图像旋转工具 (支持YOLO标签) ===")
    print("此工具将处理images文件夹中的所有jpg图像文件")
    print("每个图像将被旋转360次，每次旋转1度")
    print("同时会生成对应的YOLO格式标签文件")
    print("YOLO标签类别ID从0开始，每个图像递增")
    print()
    
    # 检查是否存在jpg图像
    jpg_pattern = "images/*.jpg"
    all_images = glob.glob(jpg_pattern)
    original_images = [img for img in all_images if 'deg.jpg' not in img]
    
    if not original_images:
        print("未找到任何jpg图像文件")
        return
    
    # 询问用户是否要查看预览
    print(f"找到 {len(original_images)} 个原始图像:")
    for i, img in enumerate(original_images):
        print(f"  {i}. {img} (将分配类别ID: {i})")
    
    print("\n选择操作:")
    print("1. 直接开始旋转所有图像（包括标签选择）")
    print("2. 先查看旋转预览")
    print("3. 退出")
    
    choice = input("请输入选择 (1-3): ").strip()
    
    if choice == "1":
        print("\n开始处理图像...")
        print("对于每个图像，您需要选择边界框（两个对角点）")
        print("注意：每个图像将生成360个旋转版本，请确保有足够的存储空间")
        confirm = input("是否继续? (y/n): ").strip().lower()
        if confirm == 'y' or confirm == 'yes':
            rotator.process_all_images()
    elif choice == "2":
        # 显示第一个图像的预览
        if original_images:
            print(f"显示 {original_images[0]} 的旋转预览...")
            rotator.create_rotation_preview(original_images[0])
            
            confirm = input("是否继续旋转所有图像? (y/n): ").strip().lower()
            if confirm == 'y' or confirm == 'yes':
                print("\n开始处理图像...")
                print("对于每个图像，您需要选择边界框（两个对角点）")
                print("注意：每个图像将生成360个旋转版本，请确保有足够的存储空间")
                confirm2 = input("是否继续? (y/n): ").strip().lower()
                if confirm2 == 'y' or confirm2 == 'yes':
                    rotator.process_all_images()
    elif choice == "3":
        print("已退出")
        return
    else:
        print("无效选择")

if __name__ == "__main__":
    main()

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

### camera_capture.py
```python
import cv2
import os

# 创建保存图像的文件夹
save_folder = "images"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 打开摄像头（默认设备索引为0）
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

print("摄像头已打开。按 'a' 键拍照，输入 'q' 退出程序。")

count = 1  # 图片计数器

while True:
    # 读取一帧画面
    ret, frame = cap.read()
    if not ret:
        print("无法读取画面")
        break

    # 显示画面（可选）
    cv2.imshow("Camera", frame)

    # 等待键盘输入
    key = cv2.waitKey(1)

    if key == ord('a'):  # 当按下 'a' 键时拍照
        filename = os.path.join(save_folder, f"image_{count:04d}.jpg")
        cv2.imwrite(filename, frame)
        print(f"已保存照片：{filename}")
        count += 1

    elif key == ord('q'):  # 按 q 键退出
        print("退出程序")
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
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
- 按提示为每张图像输入类别名称（默认使用图片文件名，可直接回车使用）。
- 按提示为每张图像用鼠标点击两个对角点，定义目标物体的边界框。
- 每张图像会自动分配一个类别ID（从0递增）。
- 工具会自动对每张图像生成360个旋转版本及对应标签。
- 自动生成 classes.txt 文件，包含所有类别名称。

### 2. 可视化旋转结果
- 运行：
```bash
python yolo_visualizer.py
```
- 选择旋转结果文件夹，可按角度采样或自定义角度查看旋转效果和标签。

### 类别ID和类别名称规则

1. **类别ID分配**：
   - 第一个图像：类别ID = 0
   - 第二个图像：类别ID = 1
   - 依此类推...

2. **类别名称规则**：
   - **默认行为**：自动使用图片文件名（去掉.jpg扩展名）作为类别名称
   - 例如：`cammel_1.jpg` → 默认类别名为 `cammel_1`

### 输出文件结构
```
output/
├── cammel_1_000.jpg            # 旋转0°图像
├── cammel_1_000.txt            # 旋转0°标签 (类别ID: 1)
├── cammel_1_001.jpg            # 旋转1°图像
├── cammel_1_001.txt            # 旋转1°标签 (类别ID: 1)
├── ...                         # cammel_1的其他旋转角度
└── classes.txt                 # YOLO类别名称文件
```

### YOLO标签格式
每个标签文件一行：
```
class_id center_x center_y width height
```
- class_id：类别ID（从0递增）
- center_x, center_y, width, height：均为归一化（0-1）

## classes.txt格式
每行一个类别名称，行号对应类别ID：
```
cammel_1
person
car
...
```
- 第0行对应类别ID 0（background）
- 第1行对应类别ID 1（cammel_1）
- 依此类推


## 示例流程
1. 将图片放入 images/ 文件夹
   - 例如：`cammel_1.jpg`
2. 运行 `python image_rotator.py`
3. 对于每张图像：
   - 输入类别名称（可直接回车使用默认名称）
   - 用鼠标点击两个对角点进行标注
4. 自动生成classes.txt和所有旋转图像及标签
5. 运行 `python yolo_visualizer.py` 检查旋转与标签效果