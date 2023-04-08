import os
import numpy as np
import glob
import cv2
import torch
import sys
sys.path.append("..")
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
from MaskUtils import MaskUtils

# 初始化模型
sam_checkpoint = "./models/sam_vit_h_4b8939.pth"
device = 'cuda' if torch.cuda.is_available() else 'cpu' # mps is faster than cpu,but mps no support for int64, float64
model_type = "default"
OutPutFolder = "output"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
sam.to(dtype=torch.float32)

sam_predictor = SamPredictor(sam)

mask_utils = MaskUtils(sam_predictor)

def process_image(image_path):
    # 打开图片并转换为numpy数组
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # input_point = np.array([[500, 375]])
    # input_label = np.array([1])

    input_point = np.array([[500, 375], [1125, 625]])
    input_label = np.array([1, 1])

    # mask_utils.show_masks_one_figure(image, input_point, input_label)
    mask_utils.show_best_mask(image, input_point, input_label)

def main():
    # 查找 /input 文件夹下的所有 .jpg 和 .png 文件（不区分大小写）
    input_folder = "input"
    image_files = []

    for ext in ('*.jpg', '*.JPG', '*.png', '*.PNG'):
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))

    # 处理每个图像文件
    for image_file in image_files:
        process_image(image_file)

if __name__ == '__main__':
    main()
