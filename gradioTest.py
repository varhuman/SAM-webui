import gradio as gr
import numpy as np
from PIL import Image

# 为了简化示例，我们创建一个虚拟的数据结构来表示图像中的物体及其颜色信息
objects = {
    (50, 50): {"color": (255, 0, 0)},
    (100, 100): {"color": (0, 255, 0)},
    (150, 150): {"color": (0, 0, 255)}
}

def highlight_object(input_image, x, y):
    # 根据用户点击的坐标找到对应的物体
    selected_object_coords = (x, y)

    # 获取物体的颜色信息
    object_color = objects[selected_object_coords]["color"]

    # 将输入图像转换为 NumPy 数组
    numpy_data = np.array(input_image)

    # 增加物体的颜色亮度（这里我们只是简单地将颜色值增加 100）
    result_image = numpy_data.copy()
    result_image[result_image == object_color] += 100

    # 返回处理后的图像
    return Image.fromarray(np.uint8(result_image))

# 创建 Gradio 界面
image_input = gr.inputs.Image()
point_input = gr.inputs.Point()
image_output = gr.outputs.Image()

iface = gr.Interface(
    fn=highlight_object,
    inputs=[image_input, point_input],
    outputs=image_output,
    title="物体高亮"
)

iface.launch()
