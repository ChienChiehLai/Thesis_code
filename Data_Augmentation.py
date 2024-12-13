from PIL import Image, ImageChops
import os

source_folder = "Data80/Test_Manual_many"
target_folder = "Data80/Test_Manual_many"


# 遍历源文件夹中的所有文件
for file_name in os.listdir(source_folder):
    # 构建完整的文件路径
    file_path = os.path.join(source_folder, file_name)
    
    # 检查文件是否是PNG图像
    if file_path.endswith('.png'):
        # 打开图像
        img = Image.open(file_path)
        # 左右翻轉
        # new_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        # base_name, ext = os.path.splitext(file_name)
        # new_file_name = f"{base_name}_0{ext}"

        # 上下翻轉
        new_img = img.transpose(Image.FLIP_TOP_BOTTOM)
        base_name, ext = os.path.splitext(file_name)
        new_file_name = f"{base_name}_1{ext}"

        # 旋轉
        # new_img = img.rotate(90, expand=True)
        # base_name, ext = os.path.splitext(file_name)
        # new_file_name = f"{base_name}_90{ext}"

        # 移動
        # offset_x = -20 # -30=往左移動30格
        # offset_y = 0
        # new_img = ImageChops.offset(img, offset_x, offset_y)
        # base_name, ext = os.path.splitext(file_name)
        # new_file_name = f"{base_name}_x20{ext}"

        # 构建目标文件的完整路径
        target_path = os.path.join(target_folder, new_file_name)
        # 保存翻转后的图像到目标文件夹
        new_img.save(target_path)


# print("All PNG images have been flipped and saved to the target folder.")

# for i in range(15,41):

#     Patient = "Patient60_"
#     slice = "slice00"+str(i)

    # image = Image.open('Data17/Train/Flair/'+Patient+slice+'.png')
    # rotated_image = image.rotate(90, expand=True)
    # rotated_image.save('Data17/Train/Flair/'+Patient+slice+'_1.png')

    # image = Image.open('Data17/Train/Flair/'+Patient+slice+'.png')
    # rotated_image = image.rotate(180, expand=True)
    # rotated_image.save('Data17/Train/Flair/'+Patient+slice+'_2.png')

    # image = Image.open('Data17/Train/Flair/'+Patient+slice+'.png')
    # rotated_image = image.rotate(270, expand=True)
    # rotated_image.save('Data17/Train/Flair/'+Patient+slice+'_3.png')

    # image = Image.open('Data17/Train/WMH/'+Patient+slice+'.png')
    # rotated_image = image.rotate(90, expand=True)
    # rotated_image.save('Data17/Train/WMH/'+Patient+slice+'_1.png')

    # image = Image.open('Data17/Train/WMH/'+Patient+slice+'.png')
    # rotated_image = image.rotate(180, expand=True)
    # rotated_image.save('Data17/Train/WMH/'+Patient+slice+'_2.png')

    # image = Image.open('Data17/Train/WMH/'+Patient+slice+'.png')
    # rotated_image = image.rotate(270, expand=True)
    # rotated_image.save('Data17/Train/WMH/'+Patient+slice+'_3.png')

    # image = Image.open('Data17/Train/Flair/'+Patient+slice+'.png')
    # flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    # flipped_image.save('Data17/Train/Flair/'+Patient+slice+'_0.png')

    # image = Image.open('Data17/Train/WMH/'+Patient+slice+'.png')
    # flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    # flipped_image.save('Data17/Train/WMH/'+Patient+slice+'_0.png')
