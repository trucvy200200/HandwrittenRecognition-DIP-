import cv2
import numpy as np
import os
# Load image and convert to grayscale
img =  cv2.imread(r'C:\Users\ACER\Pictures\Saved Pictures\Week 2\Screenshot 2023-04-20 201316.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Dilate the image to make the text more clear
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilated = cv2.dilate(thresh, kernel, iterations=2)

# Find edges
edges = cv2.Canny(dilated, 150, 250, apertureSize=3)

# Find lines
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=20, maxLineGap=100)

# Draw lines on original image
for i, line in enumerate(lines):
    x1, y1, x2, y2 = line[0]
    #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
    line_img = img[y1:y2, x1:x2]  # Crop line from original image
    # if line_img.any():
    #     cv2.imwrite(f'line_{i}.png', line_img)  # Save cropped line as a new image


# Create horizontal histogram
hist = cv2.reduce(dilated, 1, cv2.REDUCE_AVG).reshape(-1)

# Find peaks in histogram
peaks = np.where(hist >= 1)[0]

# Draw peaks on original image
def draw_peaks():
    for peak in peaks:
        cv2.line(img, (0, peak), (img.shape[1], peak), (255, 0, 0), 1)

# def cut_peaks(img, peaks, padding=10):
#     cropped_images = []
#     for peak in peaks:
#         x, y = peak[1], peak[0]
#         cropped = img[max(0, y-padding):min(img.shape[0], y+padding), max(0, x-padding):min(img.shape[1], x+padding)]
#         cropped_images.append(cropped)
#     return cropped_images

# cropped_images = cut_peaks(img, list(zip(peaks, peaks)), padding=20)
# for i, image in enumerate(cropped_images):
#     cv2.imwrite(f'cropped_{i}.png', image)

def group_peaks(peaks, max_dist):
    groups = []
    current_group = [peaks[0]]
    for i in range(1, len(peaks)):
        if peaks[i] - current_group[-1] <= max_dist:
            current_group.append(peaks[i])
        else:
            groups.append((current_group[0], current_group[-1]))
            current_group = [peaks[i]]
    groups.append((current_group[0], current_group[-1]))
    return groups

groups = group_peaks(peaks, max_dist=2)


def crop_peaks(img, groups: list):
    for group in groups:
        cropped = img[group[0]:group[1], 0:img.shape[1]]
        if cropped.any():
         cv2.imwrite(os.path.join('./data',f'cropImage-{groups.index(group)}.png'), cropped)

#cropImage = img[groups[0][0]:groups[0][1], 0:img.shape[1]]

crop_peaks(img, groups)
draw_peaks()

# Display result
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

