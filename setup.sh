#!/bin/bash

echo "Checking Python, pip, Node.js"

python --version
if [ $? -ne 0 ]; then
    echo "Error: Python is not installed or not in the PATH."
    exit 1
fi

pip --version
if [ $? -ne 0 ]; then
    echo "Error: pip is not installed or not in the PATH."
    exit 1
fi

node --version
if [ $? -ne 0 ]; then
    echo "Error: Node.js is not installed or not in the PATH."
    exit 1
fi

echo "All dependencies are present."

echo "Installing virtualenv"
pip install --user virtualenv

echo "Creating virtual environment"
python -m venv env

echo "Activating virtual environment"
source env/bin/activate

echo "Installing Python dependencies"
pip install git+https://github.com/facebookresearch/segment-anything.git
pip install opencv-python
pip install pycocotools
pip install matplotlib
pip install onnxruntime
pip install onnx
pip install gradio
pip install flask
pip install werkzeug
pip install torch torchvision 

echo "Installing Node.js dependencies"
npm install -g typescript
npm install

echo "Compiling TypeScript to JavaScript"
tsc

echo "Setup complete"
