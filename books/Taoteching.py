from constants import taoteching_input_file, input_path
from books import Books
import re


class TaoTeChing(Books):
    def __init__(self):
        super().__init__()
        self.book_name = "TaoTeChing"
        self.input_file_path = input_path+taoteching_input_file

    def fetch_data(self):
        """
        :return: returns a dict by chapters implemented by each book
        """
        req = open(self.input_file_path)
        output_dict = {}
        first_line_found = False
        chapter_name = ""
        text = ""
        for line in req.readlines():
            if not first_line_found and not line.startswith("1"):
                continue
            if re.match(r"^\d", line):
                first_line_found = True
                if chapter_name!="":
                    output_dict[chapter_name] = text
                chapter_name = int(line.replace("\n","").replace(" ","").replace("\t",""))
                text = ""
            else:
                text += line
        if chapter_name!="":
            output_dict[chapter_name] = text
        return output_dict
