import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#i是Data幾的意思
for i in [84]:
    Data_folder = "Data"+str(i)
    epoch = "epoch100"
    Test_folder = "Test_"+epoch
    Manual_folder = "Test_Manual"
    Flair_folder = "Test_Origin"
    results_df_path = Data_folder+"_"+epoch+"_6.xlsx"

    # 讀取Excel檔，如果不存在就建立一個新的
    try:
        results_df = pd.read_excel(results_df_path)
    except FileNotFoundError:
        results_df = pd.DataFrame(columns=["Patient", "Slice", "Area", "Dice", "Dice*Area"])

    # 讀取所有结果並計算各種指標
    for filename in os.listdir(os.path.join(Data_folder, Test_folder)):
        if filename.endswith("_res.png"):
            
            parts = filename.split('_')
            patient_number = parts[0][7:]
            slice_number = parts[1]
         
            manual_path = os.path.join(Data_folder, Manual_folder, f"{parts[0]}_{slice_number}.png")
            result_path = os.path.join(Data_folder, Test_folder, filename)
            flair_path = os.path.join(Data_folder, Flair_folder, f"{parts[0]}_{slice_number}.png")

            flair = mpimg.imread(flair_path)
            result = mpimg.imread(result_path)
            manual = mpimg.imread(manual_path)

            TP = np.logical_and(result > 0.1, manual > 0.1)
            FP = np.logical_and(result > 0.1, manual < 0.1)
            FN = np.logical_and(result < 0.1, manual > 0.1)
            TN = np.logical_and(result < 0.1, manual < 0.1)

            A = np.sum(TP)
            B = np.sum(FP)
            C = np.sum(FN)
            D = np.sum(TN)

            Area = A+C
            Dice = 2 * A / (2 * A + B + C) if A != 0 else 0

            new_row = pd.DataFrame({
                "Patient": [parts[0]],
                "Slice": [slice_number],
                "Area": [Area],
                "Dice": [round(Dice, 4)],
                "Dice*Area": [round(Dice*Area, 4)],
            })
            results_df = pd.concat([results_df, new_row], ignore_index=True)

            plt.figure(figsize=(9, 3))
            plt.subplot(1, 3, 1)
            plt.imshow(flair, cmap=plt.cm.gray)
            plt.axis('off')
            plt.title('Original Image')

            plt.subplot(1, 3, 2)
            plt.imshow(flair, cmap=plt.cm.gray)
            plt.contour(result > 0.1, [0], colors='r', linewidths=0.2)
            plt.axis('off')
            plt.title('Result of U-net')

            plt.subplot(1, 3, 3)
            plt.imshow(flair, cmap=plt.cm.gray)
            plt.contour(manual > 0.1, [0], colors='r', linewidths=0.2)
            plt.axis('off')
            plt.title('Gold Standard')

            plt.subplots_adjust(wspace=0, hspace=0)
            plt.figtext(0.15, 0.02, f"{parts[0]}_{slice_number}, Area = {Area}, Dice = {Dice:.4f}")
            plt.savefig(os.path.join(Data_folder, "Test_result_"+epoch, f"{parts[0]}_{slice_number}.png"), dpi=300, bbox_inches='tight', pad_inches=0.1)
            plt.close()

    # 保存更新后的DataFrame到Excel文件
    results_df.to_excel(results_df_path, index=False)