import numpy as np
import matplotlib.pyplot as plt
import cv2

image = cv2.imread("Total_Training_Data_256/Rescale2/Patient2_slice0030.png")
image2 = cv2.imread("Total_Training_Data_256/Rescale2/Patient51_slice0030.png")
# image3 = cv2.imread("Total_Training_Data_256/Singapore/Flair/Patient50_slice0001.png")
hist, bins = np.histogram(image.flatten(), 256, [0,256])
cdf = hist.cumsum()
cdf_normalized = cdf*hist.max()/cdf.max()
cdf_m = np.ma.masked_equal(cdf,0)
cdf_m = (cdf_m - cdf_m.min())*255 / (cdf_m.max() - cdf_m.min())
cdf_final = (cdf_m - cdf_m.min())*255 / (cdf_m.max() - cdf_m.min())

image_normalized = np.interp(image.flatten(), bins[:-1], cdf_final)
image_normalized = image_normalized.reshape(image.shape)

hist_normalized, bins_normalized = np.histogram(image_normalized.flatten(), 256, [0,1])
cdf_normalized_new = hist_normalized.cumsum()
cdf_normalized_new = cdf_normalized_new * hist_normalized.max() / cdf_normalized_new.max()

print(np.max(image), np.max(image_normalized))

plt.subplot(2,2,1)
plt.imshow(image, cmap="gray")
plt.xticks([]), plt.yticks([])
plt.title('Normalized Image')

plt.subplot(2,2,2)
plt.hist(image.flatten(), 256, [0, 256], color = 'lightgray')
plt.plot(bins[:-1], cdf_normalized, color = 'red', label = 'CDF')
plt.xticks([])
plt.yticks([])
plt.ylim([0, 5000])
plt.title('Normalized Histogram')

plt.subplot(2,2,3)
plt.imshow(image2, cmap="gray")
plt.xticks([]), plt.yticks([])

plt.subplot(2,2,4)
plt.hist(image2.flatten(), 256, [0, 256], color = 'lightgray')
plt.plot(bins[:-1], cdf_normalized, color = 'red', label = 'CDF')
plt.xlabel('Pixel Value')
plt.yticks([])
plt.ylim([0, 5000])

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.05, hspace=0.02, wspace=-0.12)
plt.savefig("Normalized2 Histogram", dpi=300, bbox_inches='tight', pad_inches=0.2)
plt.show()
