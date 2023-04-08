import gradio as gr
import numpy as np
from segment_anything import sam_model_registry, SamPredictor
import cv2
import torch

# 在此处保留您提供的代码以创建和初始化模型、预测器等


def get_points_from_image(img_with_points):
    # 此处的实现取决于您如何处理用户在图像上点击选择的点
    points = ... # 提取用户在图像上选择的点的实现
    return points


def process_image(image, points):
    input_point = np.array(points)
    input_label = np.ones(len(input_point))  # 假设所有点的标签都是 1
    
    mask_utils.show_best_mask(image, input_point, input_label)
    

def main_interface(input_image, points):
    image = np.array(input_image['image'])
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    mask = np.array(input_image['mask'])
    points = get_points_from_image(points)
    
    process_image(image, points)
    

image_input = gr.inputs.Image(type="numpy", label="Input Image", tool='sketch')
# points_input = gr.inputs.Image(type="numpy", label="Points", tool="point")

iface = gr.Interface(
    fn=main_interface,
    inputs=[image_input],
    outputs="image",
    title="Image Mask Generator",
    description="Upload an image and select points to generate a mask.",
)

iface.launch()
