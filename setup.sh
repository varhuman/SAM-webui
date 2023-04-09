#!/bin/bash

echo "Installing virtualenv"
pip install --user virtualenv

echo "Creating virtual environment"
python3 -m venv env

echo "Activating virtual environment"
source env/bin/activate

echo "Installing Python dependencies"
pip install git+https://github.com/facebookresearch/segment-anything.git
pip install opencv-python pycocotools matplotlib onnxruntime onnx gradio flask werkzeug torch torchvision torchaudio

echo "Installing Node.js dependencies"
npm install -g typescript
npm install

echo "Compiling TypeScript to JavaScript"
tsc

echo "Setup complete"
