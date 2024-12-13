from PIL import Image
import numpy as np
import os
from collections import Counter

def find_most_frequent_pixel_value(image_array):
    # 只考慮像素值大於30的像素
    filtered_pixels = image_array[(image_array > 120) & (image_array < 200)].flatten()
    pixel_counts = Counter(filtered_pixels)
    if pixel_counts:
        most_common_pixel_value, _ = pixel_counts.most_common(1)[0]
        return most_common_pixel_value
    else:
        return None

def rescale_image(image_path, I, output_folder):
    try:
        # 讀取並轉換圖片為numpy數組
        image = Image.open(image_path).convert('L')  # 確保轉換為灰階
        image_array = np.array(image, dtype=np.float64)
        
        # 分段應用縮放因子
        lower_mask = image_array <= I
        upper_mask = image_array > I
        
        # 對0~I的部分進行調整
        image_array[lower_mask] = image_array[lower_mask] * (61 / I)
        
        # 對I~255的部分進行調整
        image_array[upper_mask] = 61 + (image_array[upper_mask] - I) * (194 / (255 - I))
        
        # 確保像素值在合法範圍內
        image_array = np.clip(image_array, 0, 255)
        
        # 轉換回圖片並保存
        rescaled_image = Image.fromarray(image_array.astype('uint8'))
        output_path = os.path.join(output_folder, os.path.basename(image_path))
        rescaled_image.save(output_path)
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

def process_images(input_folder, output_folder, target_value=61):
    # 確保輸出資料夾存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            
            # 讀取圖片並找出像素值超過20部分中出現最多次的像素值
            image = Image.open(image_path).convert('L')
            image_array = np.array(image, dtype=np.float64)
            I = find_most_frequent_pixel_value(image_array)
            
            if I is not None:
                # 計算縮放因子並調整像素值
                rescale_image(image_path, I, output_folder)
                print(f"Processed and rescaled {filename}","I=",I)
            else:
                print(f"No pixels with value > 40 found in {filename}, skipped.")

input_folder = "NCKUHData/Median"
output_folder = "NCKUHData/Rescale2"

process_images(input_folder, output_folder)