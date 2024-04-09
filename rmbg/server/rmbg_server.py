
import os
import requests
from rmbg.utils import jpg2png_str




class TransparentBGServerCaller:
    """调用API的类
    """    
    def __init__(self):
        self.url = None
        self.folder_queue = None
        self.img_queue = None




    def process_image(self, image_path):
        """调用API处理图片

        Args:
            image_path (str): 图片的路径
        """        
        try:
            with open(image_path, "rb") as f:
                response = requests.post(self.url, files={"file": f})
            
            if response.status_code == 200:
                #output_filename = f"{os.path.basename(image_path)}".split('.jpg')[0] + ".png"
                output_filename = jpg2png_str.convert_extension(image_path)
                with open(output_filename, "wb") as output_file:
                    output_file.write(response.content)
                print(f"Image {image_path} processed successfully. Processed image saved as {output_filename}")
            else:
                print(f"Error processing image {image_path}: {response.text}")
        except Exception as e:
            print(f"Exception processing image {image_path}: {str(e)}")
    