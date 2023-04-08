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
import matplotlib.pyplot as plt
# 初始化模型
sam_checkpoint = "./models/sam_vit_h_4b8939.pth"
device = 'cuda' if torch.cuda.is_available() else 'mps'
model_type = "default"
OutPutFolder = "output"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
sam.to(dtype=torch.float32)

predictor = SamPredictor(sam)

def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))   

def process_image(image_path):
    # 打开图片并转换为numpy数组
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    predictor.set_image(image)
    input_point = np.array([[500, 375], [1125, 625]])
    input_label = np.array([1,1])

    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    # for i, (mask, score) in enumerate(zip(masks, scores)):
    #     plt.figure(figsize=(10,10))
    #     plt.imshow(image)
    #     show_mask(mask, plt.gca())
    #     show_points(input_point, input_label, plt.gca())
    #     plt.title(f"Mask {i+1}, Score: {score:.3f}", fontsize=18)
    #     plt.axis('off')
    #     plt.show()

    mask_input = logits[np.argmax(scores), :, :]  # Choose the model's best mask

    masks, _, _ = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        mask_input=mask_input[None, :, :],
        multimask_output=False,
    )

    plt.figure(figsize=(10,10))
    plt.imshow(image)
    show_mask(masks, plt.gca())
    show_points(input_point, input_label, plt.gca())
    plt.axis('off')
    plt.show() 

    # plt.figure(figsize=(10,10))
    # plt.imshow(image)
    # show_points(input_point, input_label, plt.gca())
    # plt.axis('on')
    # plt.show()  

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
