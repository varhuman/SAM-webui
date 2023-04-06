import cv2
import numpy as np
from segment_anything import SamPredictor, build_sam
from matplotlib import pyplot as plt
import gradio as gr
import torch
import matplotlib.pyplot as plt
import cv2

import torch
import torchvision
print("PyTorch version:", torch.__version__)
print("Torchvision version:", torchvision.__version__)
print("CUDA is available:", torch.cuda.is_available())

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

# 初始化模型
predictor = SamPredictor(build_sam(checkpoint="./models/sam_vit_h_4b8939.pth"))
class PointInput(gr.inputs.Image):
    def postprocess(self, x):
        if x is not None:
            x = super().postprocess(x)
            point = np.unravel_index(np.argmax(x[:,:,0]), x[:,:,0].shape)
            return point[::-1]
        else:
            return None

def segment_image(image, point):
    if image is not None and point is not None:
        # 转换图片格式
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # 使用点选取特定对象
        input_point = np.array([point[::-1]])
        input_label = np.array([1])
        masks, _, _ = predictor.predict(point_coords=input_point, point_labels=input_label)

        # 显示结果
        result_image = image.copy()
        show_mask(masks[0], result_image)
        show_points(input_point, input_label, result_image)

        return result_image
    else:
        return None

# 定义 Gradio 界面
image_input = gr.inputs.Image(label="上传图片")
point_input = PointInput(label="选择点")
image_output = gr.outputs.Image(type="numpy", label="生成结果")

iface = gr.Interface(
    fn=segment_image,
    inputs=[image_input, point_input],
    outputs=image_output,
    examples=[],
    title="图像分割",
    description="通过选择图像上的一个点来分割对象。"
)

iface.launch()