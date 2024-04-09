

import os


def get_img_path(parent_path):
    image_paths = []
    for file in os.listdir(parent_path):
        if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
            image_paths.append(os.path.join(parent_path, file))
    return image_paths
