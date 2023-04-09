@echo off

echo Checking Python, pip, Node.js

python --version 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in the PATH.
    pause
    exit /b 1
)

pip --version 2>&1
if errorlevel 1 (
    echo Error: pip is not installed or not in the PATH.
    pause
    exit /b 1
)

node --version 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in the PATH.
    pause
    exit /b 1
)

echo All dependencies are present.

echo Installing virtualenv
pip install --user virtualenv

echo Creating virtual environment
python -m venv env

echo Activating virtual environment
call env\Scripts\activate.bat

echo Installing Python dependencies
pip install git+https://github.com/facebookresearch/segment-anything.git
pip install opencv-python 
pip install pycocotools 
pip install matplotlib 
pip install onnxruntime
pip install onnx
pip install gradio
pip install flask
pip install werkzeug
pip install torch==2.0.0+cu118 torchvision==0.15.1+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

echo Installing Node.js dependencies
npm install -g typescript
npm install

echo Compiling TypeScript to JavaScript
tsc

echo Setup complete

pause