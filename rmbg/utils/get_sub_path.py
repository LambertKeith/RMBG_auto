

import os


def get_img_path(parent_path):
    """获取文件夹下图片的绝对路径

    Args:
        parent_path (str): 文件夹路径

    Returns:
        list: 返回图片路径列表
    """    
    image_paths = []
    for file in os.listdir(parent_path):
        if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
            image_paths.append(os.path.join(parent_path, file))
    return image_paths
