

def convert_extension(filename):
    """将后缀为jpg或者jpeg的字符串转换为png结尾的字符串

    Args:
        filename (str): 尾缀为jpg的文件名

    Returns:
        str: _description_
    """    
    
    if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        index = filename.lower().rfind('.jpg')  # 找到最后一个'.jpg'的索引
        if index == -1:  # 如果未找到'.jpg'，则查找'.jpeg'
            index = filename.lower().rfind('.jpeg')
        return filename[:index] + '.png'  # 替换为'.png'
    else:
        return filename  # 如果不是jpg或jpeg结尾的文件名，则不做修改


