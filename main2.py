import cv2
import numpy as np
import torch
from segment_anything import SamPredictor, show_mask, show_points, show_box
from matplotlib import pyplot as plt
from segment_anything.utils.transforms import ResizeLongestSide

# 初始化模型
predictor = SamPredictor.from_pretrained("name_of_pretrained_model")
resize_transform = ResizeLongestSide(predictor.image_encoder.img_size)

# 读取图像
image_path = "path/to/image.jpg"
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 使用点选取特定对象
input_point = np.array([[x_coord, y_coord]])
input_label = np.array([1])
masks, _, _ = predictor.predict(point_coords=input_point, point_labels=input_label)

# 显示结果
plt.figure(figsize=(10, 10))
plt.imshow(image)
show_mask(masks[0], plt.gca())
show_points(input_point, input_label, plt.gca())
plt.axis('off')
plt.show()

# 使用框选取特定对象
input_box = np.array([x1, y1, x2, y2])
masks, _, _ = predictor.predict(box=input_box[None, :])

# 显示结果
plt.figure(figsize=(10, 10))
plt.imshow(image)
show_mask(masks[0], plt.gca())
show_box(input_box, plt.gca())
plt.axis('off')
plt.show()

# 结合点和框选取特定对象
input_box = np.array([x1, y1, x2, y2])
input_point = np.array([[x_coord, y_coord]])
input_label = np.array([0])
masks, _, _ = predictor.predict(point_coords=input_point, point_labels=input_label, box=input_box)

# 显示结果
plt.figure(figsize=(10, 10))
plt.imshow(image)
show_mask(masks[0], plt.gca())
show_box(input_box, plt.gca())
show_points(input_point, input_label, plt.gca())
plt.axis('off')
plt.show()

# 图像预处理
def prepare_image(image, transform, device):
    image = transform.apply_image(image)
    image = torch.as_tensor(image, device=device.device) 
    return image.permute(2, 0, 1).contiguous()

# 批量推断
batched_input = [
     {
         'image': prepare_image(image1, resize_transform, predictor),
         'boxes': resize_transform.apply_boxes_torch(image1_boxes, image1.shape[:2]),
         'original_size': image1.shape[:2]
     },
     {
         'image': prepare_image(image2, resize_transform, predictor),
         'boxes': resize_transform.apply_boxes_torch(image2_boxes, image2.shape[:2]),
         'original_size': image2.shape[:2]
     }
]

# 运行模型
batched_output = predictor(batched_input, multimask_output=False)

# 显示结果
fig, ax = plt.subplots(1, 2, figsize=(20, 20))

ax[0].imshow(image1)
for mask in batched_output[0]['masks']:
    show_mask(mask.cpu().numpy(), ax[0], random_color=True)
ax[0].axis('off')

ax[1].imshow(image2)
for mask in batched_output[1]['masks']:
    show_mask(mask.cpu().numpy(), ax[1], random_color=True)
ax[1].axis('off')

plt.tight_layout()
plt.show()
