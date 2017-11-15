from constants import input_path, BookEccleasiasticus_file, BookEccleasiasticus_studyline
from books import Books
import re


class BookEccleasiasticus(Books):
    def __init__(self):
        super().__init__()
        self.book_name = "BookEccleasiasticus"
        self.input_file_path = input_path + BookEccleasiasticus_file

    def fetch_data(self):
        """
        :return: returns a dict by chapters implemented by each book
        """
        req = open(self.input_file_path)
        output_dict = {}
        lines = [line for line in req.readlines()]
        ch = 1
        for i,j in BookEccleasiasticus_studyline:
            text=""
            for line in lines[i:j]:
                if re.match(r"^\d.", line):
                    if text!="":
                        output_dict[ch]=text
                        ch+=1
                    text=""
                else:
                    text+=line
            if text!="":
                output_dict[ch] = text

        return output_dict
