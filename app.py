from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify, session
from image_processing import init_sam_model, process_image
import numpy as np
import torch
app = Flask(__name__)
app.secret_key = 'your_secret_key'
mask_utils = init_sam_model()

@app.route('/')
def index():
    return render_template('index.html')

from werkzeug.utils import secure_filename
import os

# Add this right after app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Add this function to your app.py
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/static/<path:filename>')
def send_static_file(filename):
    return send_from_directory('./static', filename)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Add this new route to your app.py
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        session['uploaded_image'] = filename
        return redirect(url_for('index'))
    return redirect(request.url)

@app.route('/process_points', methods=['POST'])
def process_points():
    if not 'uploaded_image' in session:
        return jsonify({'status': 'error', 'message': 'No image uploaded'})
    data = request.get_json()
    points = data['points']
    print("Received points:", points)

    # points is a dict includes x and y, just need x and y's value to a list, like this np.array([[500, 375], [1125, 625]])

    point_array = []
    label_array = []
    for point in points:
        point_array.append([point['x'], point['y']])
        label_array.append(1)
    
    input_point = np.array(point_array)
    input_label = np.array(label_array)
    # 处理图像
    image_path = os.path.join('uploads', session['uploaded_image'])

    output_image_path = process_image(image_path, mask_utils, input_point, input_label)

    return jsonify({'output_image_path': output_image_path})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
