import os
from PIL import Image
import cv2
import sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))
from init_model.init_model import models
from utils.util import CropLineImgFromTextBlock


text_block_recognizer = models()[1]


class TextBlock:

    def __init__(self, text_block):
        self._text_block = text_block
        self._block_content = None
        self._line_imgs_crop = None
        self._line_imgs_coords = None

    @property
    def block_coords(self):
        return self._text_block[0]

    @property
    def orig_img(self):
        return self._text_block[3]

    @property
    def label(self):
        return self._text_block[1]

    @property
    def score(self):
        return self._text_block[2]

    @property
    def block_content(self):
        if self._block_content is None:
            self._block_content = text_block_recognizer(Image.fromarray(self.orig_img), lang='vie')[:-1].replace("\n", " ")
        return self._block_content

    @property
    def line_imgs_crops(self):
        if self._line_imgs_crop is None:
            self._line_imgs_crop = CropLineImgFromTextBlock(self.orig_img).lines_infor[0]
            return self._line_imgs_crop

    @property
    def line_imgs_coords(self):
        if self._line_imgs_coords is None:
            self._line_imgs_coords = CropLineImgFromTextBlock(self.orig_img).lines_infor[1]
            return self._line_imgs_coords

    @property
    def is_unnesessary(self):
        check_list = ["Hình", "hình", "Hinh", "hinh"]
        unncsr = False
        if self.block_content.__len__() >= 6:
            for check_it in check_list:
                if check_it in self.block_content and self.block_content[5].isdecimal():
                    unncsr = True
                    break
        return unncsr 
