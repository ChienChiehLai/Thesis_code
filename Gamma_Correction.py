from PIL import Image
import numpy as np
import os
from collections import Counter

def find_most_frequent_pixel_value(image_array):
    # 只考慮像素值大於30的像素
    filtered_pixels = image_array[(image_array > 40) & (image_array < 100)].flatten()
    pixel_counts = Counter(filtered_pixels)
    if pixel_counts:
        most_common_pixel_value, _ = pixel_counts.most_common(1)[0]
        return most_common_pixel_value
    else:
        return None

def gamma_correction(image_path, output_folder, I):
    try:
        image = Image.open(image_path).convert('L')
        image_array = np.array(image, dtype=np.float32) / 255.0
        
        # 計算 Gamma 值
        target = 61 / 255.0
        gamma = np.log(target) / np.log(I / 255.0)
        
        # 應用 Gamma 轉換
        corrected_image_array = 255.0 * np.power(image_array, gamma)
        corrected_image_array = np.clip(corrected_image_array, 0, 255)  # 保證像素值在有效範圍內
        
        # 轉換回圖片並保存
        corrected_image = Image.fromarray(np.uint8(corrected_image_array))
        output_path = os.path.join(output_folder, os.path.basename(image_path))
        corrected_image.save(output_path)
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
                gamma_correction(image_path, output_folder, I)
                print(f"Processed and rescaled {filename}","I=",I)
            else:
                print(f"No pixels with value > 30 found in {filename}, skipped.")

input_folder = "NCKUH/BRAINMRI_094"
output_folder = "NCKUH/Rescale3"

process_images(input_folder, output_folder)