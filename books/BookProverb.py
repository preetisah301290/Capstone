from constants import input_path, BookProverb_studyline, BookProverb_file
from books import Books
import re


class BookProverb(Books):
    def __init__(self):
        super().__init__()
        self.book_name = "BookProverb"
        self.input_file_path = input_path + BookProverb_file

    def fetch_data(self):
        """
        :return: returns a dict by chapters implemented by each book
        """
        req = open(self.input_file_path)
        output_dict = {}
        lines = [line for line in req.readlines()]
        ch = 0
        for i,j in BookProverb_studyline:
            text=""
            for line in lines[i:j]:
                    text+=line
            ch+=1
            output_dict[ch] = text
        import pdb;pdb.set_trace()
        return output_dict
