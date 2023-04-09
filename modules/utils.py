import cv2
import os

def rescale_points(points, original_size, displayed_size):
    width_ratio = original_size['width'] / displayed_size['width']
    height_ratio = original_size['height'] / displayed_size['height']

    scaled_points = []
    for point in points:
        scaled_point = {}
        scaled_point['x'] = int(point['x'] * width_ratio)
        scaled_point['y'] = int(point['y'] * height_ratio)
        scaled_points.append(scaled_point)

    return scaled_points

def get_image_size(image_path):
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    res = {}
    res['width'] = width
    res['height'] = height
    return res

def check_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_new_path_if_exist(path, is_file = False, count = 1):
    if not os.path.exists(path):
        return path
    if is_file:
        path = path.split('.')
        if count > 1:
            suffix_count = len(path[0].split('_'))
            path[0] = path[0][:-suffix_count]
        path[0] = path[0] + f'_{count}'
        path = '.'.join(path)
        return get_new_path_if_exist(path, is_file, count + 1)
    else:
        if os.path.exists(path):
            if count > 1:
                suffix_count = len(path.split('_'))
                path = path[:-suffix_count]
            path = path + f'_{count}'
            return get_new_path_if_exist(path, is_file, count + 1)


