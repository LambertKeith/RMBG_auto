import yaml

def read_yaml_file(file_path=r"rmbg\config\rmbg_config.yaml"):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print("File not found.")
        return None
    except yaml.YAMLError as e:
        print("Error reading YAML file:", e)
        return None

