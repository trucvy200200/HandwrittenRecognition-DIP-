import cv2
import numpy as np
import os



# display the image with lines


# # Draw lines on original image
# for i, line in enumerate(lines):
#     x1, y1, x2, y2 = line[0]
#     print((x2, y2))
#     #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
#     line_img = img[y1:y2, x1:x2]  # Crop line from original image
#     if line_img.any():
#         cv2.imwrite(f'line_{i}.png', line_img)  # Save cropped line as a new image





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


# groups = group_peaks(peaks, max_dist=2)



# crop_peaks(img, groups)
# draw_peaks()

# Display result
# cv2.imshow('Result', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

class Extract:
    def __init__(self) -> None:
        self.img = None
        self.outputPath = None
        self.initOutput()
        pass

    def initOutput(self):
        output = "output"
        currentPath = os.path.dirname(os.path.abspath(__file__))

        if not os.path.exists(os.path.join(currentPath, output)):
            os.mkdir(os.path.join(currentPath, output))

        else:
            for file in os.listdir(os.path.join(currentPath, output)):
                os.remove(os.path.join(currentPath, output, file))

        # if os.path.exists(os.path.join(currentPath, output)):
        #     # remove this folder
        #     os.rmdir(os.path.join(currentPath, output))

        # os.mkdir(os.path.join(currentPath, output))

        self.outputPath = os.path.join(currentPath, output)

    def loadImage(self, path: str = None, image: np.ndarray = None):
        # Load image and convert to grayscale
        if not path:
            self.img =  cv2.imread(r'C:\Users\nem\Downloads\SCHOOL STUFF\HK2-2022\Digital Image Processing\Project\images\340903505_936007657849312_6748790213227131243_n.jpg')
        else:
            print("Path", path)
            self.img = cv2.imread(path)

        if image is not None:
            self.img = image
        
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        self.thresh = cv2.threshold(self.gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    def clear(self):
        # Dilate the image to make the text more clear
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        self.dilated = cv2.dilate(self.thresh, self.kernel, iterations=2)

    def edge(self):
        # Find edges
        self.edges = cv2.Canny(self.dilated, 50, 150, apertureSize=3)

    def findLines(self):
        # Find lines
        self.lines = cv2.HoughLinesP(self.edges, 1, np.pi/180, threshold=100, minLineLength=20, maxLineGap=100)


    def histogram(self):
        # Create horizontal histogram
        self.hist = cv2.reduce(self.dilated, 1, cv2.REDUCE_AVG).reshape(-1)

    def findPeaks(self):
        # Find peaks in histogram
        self.peaks = np.where(self.hist >= 17)[0]

    def preProcessing(self):
        # self.loadImage()
        self.clear()
        self.edge()
        self.findLines()
        self.histogram()
        self.findPeaks()
        # self.draw_peaks()

    # Draw peaks on original image
    def draw_peaks(self):
        for peak in self.peaks:
            cv2.line(self.img, (0, peak), (self.img.shape[1], peak), (255, 0, 0), 1)

    def group_peaks(self, peaks, max_dist) -> list:
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

    def crop_peaks(self, img, groups: list) -> list:

        cropped_groups = []

        for group in groups:
            cropped = img[group[0]:group[1], 0:img.shape[1]]
            if cropped.any():
                outputPath = os.path.join(self.outputPath, f'cropImage-{groups.index(group)}.png')

                cv2.imwrite(outputPath, cropped)
                cropped_groups.append(cropped)

        return cropped_groups


if __name__ == "__main__":
    # ex = Extract()
    # ex.preProcessing()

    # groups = ex.group_peaks()

    pass