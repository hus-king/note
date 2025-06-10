# 针对32张已知 CIFAR-100 图像的分类模型训练与推理指南

本文档包含两个主要部分：**训练脚本**和**推理脚本**。  
我们使用 **ResNet-18** 构建一个针对 16 类、共 32 张图像的小样本分类模型，并对其进行训练和测试。

---

## 🧠 模型训练

### 文件结构要求

请确保你的数据集目录结构如下：

```
./dataset/
    ├── class1/
    │   ├── img1.png
    │   └── img2.png
    ├── class2/
    │   ├── img1.png
    │   └── img2.png
    ...
    └── class16/
        ├── img1.png
        └── img2.png
```

每个类别下有 2 张图片，总共 32 张图像。

### 训练流程说明

- 使用 `CustomImageDataset` 自定义加载器读取数据；
- 应用基本的预处理（Resize 到 224x224 并转为 Tensor）；
- 加载预训练 ResNet-18 模型，并将最后的全连接层替换为适用于 16 类输出的线性层；
- 冻结主干网络参数，仅训练最后一层；
- 使用 Adam 优化器进行微调；
- 进行 50 轮训练后保存模型权重；
- 最后在训练集上进行测试并输出预测结果。

### ✅ 训练代码

```python
import os
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from torch.utils.data import Dataset, DataLoader

# 自定义数据集
class CustomImageDataset(Dataset):
    def __init__(self, root, transform=None):
        self.root = root
        self.transform = transform
        self.classes = sorted(os.listdir(root))
        self.class_to_idx = {c: i for i, c in enumerate(self.classes)}
        self.samples = [
            (os.path.join(root, c, f), self.class_to_idx[c])
            for c in self.classes for f in os.listdir(os.path.join(root, c))
        ]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        image = Image.open(path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label


# 数据增强与加载
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

dataset = CustomImageDataset(root='./dataset', transform=transform)
loader = DataLoader(dataset, batch_size=4, shuffle=True)

# 模型构建
model = models.resnet18(weights="IMAGENET1K_V1")
model.fc = nn.Linear(512, len(dataset.classes))
model = model.cuda()

# 冻结主干网络
for param in model.parameters():
    param.requires_grad = False
model.fc.requires_grad_(True)

# 训练配置
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=1e-3)

# 训练循环
model.train()
for epoch in range(50):
    for images, labels in loader:
        images, labels = images.cuda(), labels.cuda()
        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
# 训练结束后保存模型
torch.save(model.state_dict(), "resnet18_custom.pth")
print("Model saved to resnet18_custom.pth")

# 测试
model.eval()
with torch.no_grad():
    for images, labels in loader:
        images, labels = images.cuda(), labels.cuda()
        outputs = model(images)
        predicted = torch.argmax(outputs, dim=1)
        print("Labels:", labels)
        print("Predicted:", predicted)
```

---

## 🔍 模型推理

推理脚本用于对测试文件夹中的图像进行分类预测。

### 文件结构要求

请确保你的测试图像存放在如下路径中：

```
./test/
    ├── test1.png
    ├── test2.png
    └── ...
```

这些图像应为训练时使用的相同 32 张图像。

### 推理流程说明

- 重新构造与训练一致的 ResNet-18 网络结构；
- 加载之前训练保存的模型权重；
- 使用 CPU 进行推理；
- 对每张图片进行预处理并预测其所属类别；
- 输出图像名称及对应的预测类别名称。

### ✅ 推理代码

```python
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import os

# 类别数量（根据你的数据集调整）
num_classes = 16  # 与权重文件保持一致

# 加载模型结构
model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(512, num_classes)

# 加载训练好的权重
model.load_state_dict(torch.load("resnet18_custom.pth", map_location=torch.device('cpu')))
model = model.cpu()  # 使用 CPU
model.eval()

# 图像预处理（必须与训练时一致）
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# 类别索引到类别名称的映射
class_names = [
    "camel",
    "chair",
    "dolphin",
    "hamster",
    "lion",
    "maple_tree",
    "orange",
    "orchid",
    "pickup_truck",
    "pine",
    "rabbit",
    "skyscraper",
    "squirrel",
    "tractor",
    "turtle",
    "willow_tree"
]

# 推理函数
def predict_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)  # 不再移到 GPU
    with torch.no_grad():
        output = model(image)
        predicted_idx = torch.argmax(output, dim=1).item()
    return predicted_idx

# 示例调用
if __name__ == "__main__":
    test_dir = "./test"
    for fname in os.listdir(test_dir):
        if fname.lower().endswith(".png"):
            image_path = os.path.join(test_dir, fname)
            predicted_class = predict_image(image_path)
            print(f"{fname}: {class_names[predicted_class]}")
```

---

## 📌 总结

该文档提供了一个完整的训练与推理流程，适用于小样本图像分类任务。尽管数据量极小（仅 32 张图像），但通过迁移学习和冻结主干网络的方式，仍然可以实现快速有效的训练与预测。

如需扩展至更多类别或更大规模数据集，请相应地调整输入路径、类别数以及模型结构。