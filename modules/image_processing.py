import os
import numpy as np
import cv2
import torch
import sys
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
from modules.mask_utils import MaskUtils

def init_sam_model():
    # 初始化模型
    sam_checkpoint = "./models/sam_vit_h_4b8939.pth"
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model_type = "default"
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)
    sam.to(dtype=torch.float32)

    sam_predictor = SamPredictor(sam)

    mask_utils:MaskUtils = MaskUtils(sam_predictor)
    return mask_utils

def process_image(image_path, mask_utils:MaskUtils, input_point, input_label, save_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return mask_utils.show_best_mask(image, input_point, input_label, save_path=save_path)
