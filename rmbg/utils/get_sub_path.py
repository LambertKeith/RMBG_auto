

import os


def get_img_path(parent_path):
    image_paths = []
    for root, dirs, files in os.walk(parent_path):
        for file in files:
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
                image_paths.append(os.path.join(root, file))
    return image_paths
