import os

def get_file_size_in_mb(file_path):
    """
    计算文件大小，并以MB为单位输出

    参数:
    file_path (str): 文件路径

    返回:
    float: 文件大小 (MB)
    """
    try:
        if not os.path.isfile(file_path):
            raise ValueError("指定的路径不是一个文件")

        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)  # 转换为MB
        return round(file_size_mb, 2)
        return 
    except Exception as e :
        import traceback; traceback.print_exc();
        return None
