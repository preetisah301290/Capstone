from constants import input_path, BookWisdom_file, BookWisdom_studyline
from books import Books
import re


class BookWisdom(Books):
    def __init__(self):
        super().__init__()
        self.book_name = "BookWisdom"
        self.input_file_path = input_path + BookWisdom_file

    def fetch_data(self):
        """
        :return: returns a dict by chapters implemented by each book
        """
        req = open(self.input_file_path)
        output_dict = {}
        lines = [line for line in req.readlines()]
        ch = 0
        for i,j in BookWisdom_studyline:
            text=""
            for line in lines[i:j]:
                    text+=line
            ch+=1
            output_dict[ch] = text
        return output_dict
