import gradio as gr

def get_click_coordinates(image):
    x, y = image.shape[0], image.shape[1]
    coordinates = []

    for i in range(x):
        for j in range(y):
            if image[i, j] != 0:
                coordinates.append((i, j))

    return str(coordinates)

image_input = gr.inputs.Image(shape=(200, 200), source="canvas", label="Click on the image")
output_text = gr.outputs.Textbox(label="Clicked coordinates")

iface = gr.Interface(fn=get_click_coordinates, inputs=image_input, outputs=output_text)
iface.launch()
