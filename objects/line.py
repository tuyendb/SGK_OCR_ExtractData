import cv2
import os
import sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))


class Line:

    def __init__(self, img, line_coord, line_ct):
        self._img = img
        self._line_coord = line_coord
        self._line_ct = line_ct
        self._line_img_crop = None
        self._binary_img = None
        self._text_height = None
        self._line_img_shape = None
        self._x_cooords = None
    
    @property
    def line_content(self):
        line = ''
        for word in self._line_ct:
            line += word + ' '
        return line
    
    @property
    def line_img_crop(self):
        if self._line_img_crop is None:
            x1, y1, x2, y2 = self._line_coord
            self._line_img_crop = self._img[y1:y2, x1:x2]
        return self._line_img_crop
    
    @property
    def line_img_shape(self):
        if self._line_img_shape is None:
            self._line_img_shape = self.line_img_crop.shape[:2]
        return self._line_img_shape

    @property
    def binary_img(self):
        if self._binary_img is None:
            gray_img = cv2.cvtColor(self.line_img_crop.copy(), cv2.COLOR_BGR2GRAY)
            self._binary_img = cv2.threshold(gray_img.copy(), 200, 255, cv2.THRESH_BINARY)[1]
        return self._binary_img
    
    @property
    def text_height(self):
        if self._text_height is None:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 1))
            erode_img = cv2.erode(self.binary_img.copy(), kernel, iterations=3)
            above_point = below_point = None
            for i1 in range(self.line_img_shape[0]):
                for j1 in range(int(self.line_img_shape[1] / 2)):
                    if 255 not in erode_img[i1, j1:j1 + int(self.line_img_shape[1] / 2) + 1]:
                        above_point = i1
                        break
                if above_point is not None:
                    break
            for i2 in range(self.line_img_shape[0]):
                for j2 in range(int(self.line_img_shape[1] / 2)):
                    if 255 not in erode_img[-i2 - 1, j2:j2 + int(self.line_img_shape[1] / 2) + 1]:
                        below_point = self.line_img_shape[0] - i2 - 1
                        break
                if below_point is not None:
                    break
            if below_point is None or above_point is None:
                self._text_height = 0
            else:
                self._text_height = round((below_point - above_point), 1)
        return self._text_height

    @property
    def x_cooords(self):
        if self._x_cooords is None:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
            erode_img = cv2.erode(self.binary_img.copy(), kernel=kernel, iterations=1)
            center_y = int(self.line_img_shape[0] / 2)
            center_line = erode_img[center_y:center_y + 1, 0:self.line_img_shape[1]].flatten()
            start_point = end_point = 0
            for i in range(0, self.line_img_shape[1] - 1):
                if center_line[i] == 0 and center_line[i + 1] == 0:
                    start_point = i
                    break
            for j in range(1, self.line_img_shape[1]):
                if center_line[-j] == 0 and center_line[-j - 1] == 0:
                    end_point = self.line_img_shape[1] - j
                    break
            self._x_coords = (start_point + self._line_coord[0], end_point + self._line_coord[0])
        return self._x_coords
