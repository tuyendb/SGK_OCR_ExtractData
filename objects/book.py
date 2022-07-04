import os
import sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))
from utils.util import pdf2jpg


class Book:

    def __init__(self, pdf_path, first_page, last_page):
        self._pdf_path = pdf_path
        self._first_page = first_page
        self._last_page = last_page

    @property
    def pages(self):
        return pdf2jpg(self._pdf_path, self._first_page, self._last_page)