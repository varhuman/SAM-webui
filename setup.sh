#!/bin/bash

pip install --user virtualenv
python3 -m venv env
source env/bin/activate
pip install git+https://github.com/facebookresearch/segment-anything.git
pip install opencv-python pycocotools matplotlib onnxruntime onnx gradio
