from constants import input_path, roman_numeral, upnishad_studyline, upnishad_file
from books import Books


class Upnishad(Books):
    def __init__(self):
        super().__init__()
        self.book_name = "Upnishad"
        self.input_file_path = input_path+upnishad_file

    def fetch_data(self):
        """
        :return: returns a dict by chapters implemented by each book
        """
        req = open(self.input_file_path)
        output_dict = {}
        lines = [line for line in req.readlines()]
        ch = 1
        for i,j in upnishad_studyline:
            text=""
            for line in lines[i:j]:
                if line.strip() in roman_numeral:
                    if text!="":
                        output_dict[ch]=text
                        ch+=1
                    text=""
                else:
                    text+=line
            if text!="":
                output_dict[ch] = text

        return output_dict
