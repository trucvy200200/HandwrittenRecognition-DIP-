import cv2
import numpy as np
import os
from cv2 import Mat


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

    def findPeaks(self, peakParam: int):
        # Find peaks in histogram
        self.peaks = np.where(self.hist >= peakParam)[0]
        # print("self.peaks", self.peaks)


    def preProcessing(self):
        # self.loadImage()
        self.clear()
        self.edge()
        self.findLines()
        self.histogram()
        peakParam = self.findPeakParameter()
        print("peakParam", peakParam)
        self.findPeaks(peakParam)
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

    def crop_peaks(self, img: Mat, groups: list, export: bool = True) -> list:

        cropped_groups = []

        for group in groups:
            cropped = img[group[0]:group[1], 0:img.shape[1]]

            if cropped.any():
                if export:
                    outputPath = os.path.join(self.outputPath, f'cropImage-{groups.index(group)}.png')
                    cv2.imwrite(outputPath, cropped)
                    cropped_groups.append(cropped)
                else:
                    cropped_groups.append((group[0], group[1]))
        return cropped_groups

    def findPeakParameter(self):
        for i in range(15, 4, -1):
            try:
                self.peaks = np.where(self.hist >= i)[0]
                groups = self.group_peaks(self.peaks, max_dist=2)
                cropped_groups = self.crop_peaks(self.img, groups, export=False)

                # Calculate avg distance between peaks
                sum_dist = 0
                for group in cropped_groups:
                    sum_dist += (group[1] - group[0])

                avg_dist = sum_dist / len(cropped_groups)

                if self.peakStatisfy(cropped_groups, avg_dist):
                    return i

            except Exception as e:
                print("findPeakParameter", e)
                continue

    def peakStatisfy(self, cropped_groups: list, avg_dist: float):
        for group in cropped_groups:
                if (group[1] - group[0]) / avg_dist < 0.35:
                    return False
  
        return True

if __name__ == "__main__":
    # ex = Extract()
    # ex.preProcessing()

    # groups = ex.group_peaks()

    pass