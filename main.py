import os
import numpy as np
from segment_anything import build_sam, SamPredictor
from PIL import Image
import glob

# 初始化模型
predictor = SamPredictor(build_sam(checkpoint="./models/sam_vit_h_4b8939.pth"))

def process_image(image_path):
    # 打开图片并转换为numpy数组
    image = Image.open(image_path)
    numpy_data = np.asarray(image)

    # 设置图片
    predictor.set_image(numpy_data)

    # 设置一个前景点提示，这里使用图片中心
    point_coords = np.array([[numpy_data.shape[1] // 2, numpy_data.shape[0] // 2]])
    point_labels = np.array([1])  # 前景点提示

    # 预测并获取结果
    masks, _, _ = predictor.predict(point_coords=point_coords, point_labels=point_labels, multimask_output=False)

    # 获取最佳预测掩码（在这个例子中只有一个）
    best_mask = masks[0]

    # 将 best_mask 扩展为与 numpy_data 相同的形状
    best_mask = np.stack([best_mask] * 3, axis=-1)

    # 将掩码与原始图像合成
    result_image = np.multiply(numpy_data, best_mask)

    # 创建 output 文件夹（如果不存在）
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 将结果保存到 output 文件夹中，文件名与输入文件相同
    file_name = os.path.basename(image_path)
    output_path = os.path.join(output_folder, file_name)
    Image.fromarray(result_image.astype(np.uint8)).save(output_path)
    print(f"Processed image saved as {output_path}")

def main():
    # 查找当前目录下的所有.jpg和.png文件
    image_files = glob.glob('*.jpg') + glob.glob('*.png')

    # 处理每个图像文件
    for image_file in image_files:
        process_image(image_file)

if __name__ == '__main__':
    main()
