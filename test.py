import os
import numpy as np
from PIL import Image
import glob
import cv2

import sys
sys.path.append("..")
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

# 初始化模型
sam_checkpoint = "./models/sam_vit_h_4b8939.pth"
device = "cuda"
model_type = "default"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

mask_generator = SamAutomaticMaskGenerator(sam)

def process_image(image_path):
    # 打开图片并转换为numpy数组
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 根据输入图像生成多个区域掩码
    masks = mask_generator.generate(image)

    # 创建一个空白图像，用于存储融合的结果
    result_image = np.zeros_like(image, dtype=np.float32)
    
    # 创建 output 文件夹（如果不存在）
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历每个掩码并将其保存为图像
    for i, mask in enumerate(masks):
        # 为当前掩码生成随机颜色
        color = np.random.randint(0, 256, size=(3,))

        # 将 mask 扩展为与 image 相同的形状
        mask_expanded = np.stack([mask['segmentation']] * 3, axis=-1)

        # 将掩码与随机颜色相乘
        colored_mask = mask_expanded * color

        # 将彩色掩码与结果图像融合
        result_image += colored_mask

        # 将掩码与原始图像合成
        resultone_image = np.multiply(image, mask_expanded)

        file_name = os.path.splitext(os.path.basename(image_path))[0]
        outputone_folder = os.path.join(output_folder, f"{file_name}")
        if not os.path.exists(outputone_folder):
            os.makedirs(outputone_folder)
        path = os.path.join(outputone_folder, f"{file_name}_mask_{i}.png")
        Image.fromarray(resultone_image.astype(np.uint8)).save(path)
        print(f"Processed image saved as {path}")

    # 将结果图像裁剪到 [0, 255] 范围内并转换为 uint8
    result_image = np.clip(result_image, 0, 255).astype(np.uint8)

    # 将结果保存到 output 文件夹中，文件名与输入文件相同
    file_name = os.path.basename(image_path)
    output_path = os.path.join(output_folder, file_name)
    Image.fromarray(result_image).save(output_path)
    print(f"Processed image saved as {output_path}")

def main():
    # 查找 /input 文件夹下的所有 .jpg 和 .png 文件
    input_folder = "input"
    image_files = glob.glob(os.path.join(input_folder, '*.jpg')) + glob.glob(os.path.join(input_folder, '*.png'))


    # 处理每个图像文件
    for image_file in image_files:
        process_image(image_file)

if __name__ == '__main__':
    main()
