""" import os
import requests
import concurrent.futures
import time

# Function to process a single image
def process_image(image_path):
    try:
        with open(image_path, "rb") as f:
            response = requests.post(url, files={"file": f})
        
        if response.status_code == 200:
            output_filename = f"processed_{os.path.basename(image_path)}"
            with open(output_filename, "wb") as output_file:
                output_file.write(response.content)
            print(f"Image {image_path} processed successfully. Processed image saved as {output_filename}")
        else:
            print(f"Error processing image {image_path}: {response.text}")
    except Exception as e:
        print(f"Exception processing image {image_path}: {str(e)}")

# 记录开始时间
start_time = time.time()

# Set the URL for the FastAPI service
url = "http://localhost:8000/remove_background/"

# List of image paths
image_paths = [r"\\192.168.10.229\摄影部\千百度男鞋\商务\2024\4月\4.8 白底\C0142151LA24\D-8E9A6835.jpg", 
               r"\\192.168.10.229\摄影部\千百度男鞋\商务\2024\4月\4.8 白底\C0142151LA24\D-8E9A6836.jpg", 
               r"\\192.168.10.229\摄影部\千百度男鞋\商务\2024\4月\4.8 白底\C0142151LA24\D-8E9A6839.jpg"
               ]

# Create a thread pool executor
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit the processing of each image to the executor
    futures = [executor.submit(process_image, path) for path in image_paths]
    
    # Wait for all tasks to complete
    for future in concurrent.futures.as_completed(futures):
        future.result()

print("All images processed.")
# 记录结束时间
end_time = time.time()

# 计算函数运行时间
execution_time = end_time - start_time
print("Function execution time:", execution_time, "seconds") """

import os
import requests
import time
import os
import requests
import threading

# 定义处理图片的函数
def process_image(image_path):
    try:
        with open(image_path, "rb") as f:
            response = requests.post(url, files={"file": f})
        
        if response.status_code == 200:
            output_filename = f"{os.path.basename(image_path)}".split('.jpg')[0] + ".png"
            with open(output_filename, "wb") as output_file:
                output_file.write(response.content)
            print(f"Image {image_path} processed successfully. Processed image saved as {output_filename}")
        else:
            print(f"Error processing image {image_path}: {response.text}")
    except Exception as e:
        print(f"Exception processing image {image_path}: {str(e)}")

# 设置FastAPI服务的URL
url = "http://localhost:8000/remove_background/"

# 图片路径列表
image_paths = [r"\\192.168.10.229\摄影部\千百度男鞋\商务\2024\4月\4.8 白底\C0142151LA24\D-8E9A6835.jpg", 

]

# 创建线程列表
threads = []
# 记录开始时间
start_time = time.time()

# 启动线程调用处理函数
for image_path in image_paths:
    thread = threading.Thread(target=process_image, args=(image_path,))
    threads.append(thread)
    thread.start()

# 等待所有线程结束
for thread in threads:
    thread.join()

print("All images processed.")

# 记录结束时间
end_time = time.time()

# 计算函数运行时间
execution_time = end_time - start_time
print("All images processed.")
print("Function execution time:", execution_time, "seconds")
