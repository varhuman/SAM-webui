@echo off

pip install --user virtualenv
python -m venv env
call env\Scripts\activate.bat
pip install git+https://github.com/facebookresearch/segment-anything.git
pip install opencv-python pycocotools matplotlib onnxruntime onnx gradio
