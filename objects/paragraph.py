import os
import sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))


class Paragraph:

    def __init__(self, img, para_info):
        self._para_info = para_info
        self._img = img
        self._lines_coords = None
        self._lines_ct = None
        self._paragr_coord = None
        
    @property
    def lines_ct(self):
        if self._lines_ct is None:
            self._lines_ct = self._para_info[0]
        return self._lines_ct

    @property
    def lines_coords(self):
        if self._lines_coords is None:
            self._lines_coords = self._para_info[1]
        return self._lines_coords  

    @property
    def paragraph_content(self):
        paragraph = ''
        for line in self.lines_ct:
            for word in line:
                paragraph += word + ' '
        return paragraph
    
    @property
    def paragraph_coord(self):
        if self._paragr_coord is None:
            x1 = min([f[0] for f in self.lines_coords])
            y1 = self.lines_coords[0][1]
            x2 = max([f[2] for f in self.lines_coords])
            y2 = self.lines_coords[-1][3]
            self._paragr_coord = [x1, y1, x2, y2]
        return self._paragr_coord
    
    @property
    def paragraph_img_crop(self):
        x1, y1, x2, y2 = self.paragraph_coord
        paragr_img = self._img[y1:y2, x1:x2]
        return paragr_img
        