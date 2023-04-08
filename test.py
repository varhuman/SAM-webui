import os
import numpy as np
from PIL import Image
import glob
import cv2
import time
import torch
import sys
sys.path.append("..")
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

print(torch.__version__)
# 初始化模型
sam_checkpoint = "./models/sam_vit_h_4b8939.pth"
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_type = "default"
OutPutFolder = "output"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
sam.to(dtype=torch.float32)

mask_generator = SamAutomaticMaskGenerator(sam)

def check_floder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def move_processed_input(input_path, output_folder):
    file_name = os.path.basename(input_path)
    file_folder = os.path.splitext(file_name)[0]

    output_path = os.path.join(output_folder, file_folder)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    moved_image_path = os.path.join(output_path, file_name)
    os.rename(input_path, moved_image_path)

def process_image(image_path):
    # 打开图片并转换为numpy数组
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # get image_path name
    file_name = os.path.splitext(os.path.basename(image_path))[0]
    # 创建 output 文件夹（如果不存在）
    image_folder = os.path.join(OutPutFolder, file_name)
    check_floder(image_folder)

    # 获取当前时间戳
    start_time = time.time()

    # 根据输入图像生成多个区域掩码
    masks = mask_generator.generate(image)

    # 获取当前时间戳并计算消耗时间
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Time elapsed for mask_generator.generate{file_name}: {elapsed_time:.2f} seconds")

    # 创建一个空白图像，用于存储融合的结果
    result_image = np.zeros_like(image, dtype=np.float32)

    slice_count = 0
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

        output_slice_folder = os.path.join(image_folder, f"{file_name}")

        check_floder(output_slice_folder)
        path = os.path.join(output_slice_folder, f"{file_name}_mask_{i}.png")
        Image.fromarray(resultone_image.astype(np.uint8)).save(path)
        slice_count += 1
        

    # 将结果图像裁剪到 [0, 255] 范围内并转换为 uint8
    result_image = np.clip(result_image, 0, 255).astype(np.uint8)

    # 将结果保存到 output 文件夹中，文件名与输入文件相同
    file_name = os.path.basename(image_path)
    output_path = os.path.join(image_folder, f"{file_name}_result.png")
    Image.fromarray(result_image).save(output_path)
    # 移动已处理的输入图像到 output 文件夹
    move_processed_input(image_path, OutPutFolder)
    print(f"Processed image saved as {file_name}, {slice_count} slices.")

def main():
    # 查找 /input 文件夹下的所有 .jpg 和 .png 文件（不区分大小写）
    input_folder = "input"
    image_files = []

    # 创建 output 文件夹（如果不存在）
    check_floder(OutPutFolder)

    for ext in ('*.jpg', '*.JPG', '*.png', '*.PNG'):
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))

    # 处理每个图像文件
    for image_file in image_files:
        process_image(image_file)

if __name__ == '__main__':
    main()
