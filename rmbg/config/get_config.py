import yaml

def read_yaml_file(file_path=r"rmbg\config\rmbg_config.yaml"):
    """读取配置文件

    Args:
        file_path (regexp, optional): 配置文件的路径. Defaults to r"rmbg\config\rmbg_config.yaml".

    Returns:
        _type_: _description_
    """    
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except UnicodeDecodeError:
        # 如果编码错误，强制使用utf-8
        with open(file_path, 'r', encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return data        
    except FileNotFoundError:
        print("File not found.")
        return None
    except yaml.YAMLError as e:
        print("Error reading YAML file:", e)
        return None


brand_folder = read_yaml_file(r"\\192.168.10.229\图片\批量抠图\配置文件(勿动).yaml")