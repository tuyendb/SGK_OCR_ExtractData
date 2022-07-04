import os
import sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))
from utils.util import TextBlockDetection, check_limited_area, remove_figure
from init_model.init_model import models
from objects.text_block import TextBlock


text_block_detector = models()[0]


class Page:
    
    def __init__(self, page_img):
        self._page_img = page_img
        self._text_blocks = None
        self._edited_page = None

    @property
    def text_blocks(self) -> list:
        if self._text_blocks is None:
            self._text_blocks = TextBlockDetection(self._page_img, text_block_detector).text_block_detection
        return self._text_blocks

    @property
    def edited_page(self) -> tuple:
        if self._edited_page is None:
            titles = []
            removed_fg_img = None
            for tb in self.text_blocks:
                if tb[1] == 'figure':
                    removed_fg_img = remove_figure(self._page_img.copy(), tb[0])
                elif tb[1] == 'title':
                    titles.append(tb)
            if removed_fg_img is not None:
                self._edited_page = (removed_fg_img, titles)
            else:
                self._edited_page = (self._page_img, titles)
        return self._edited_page
