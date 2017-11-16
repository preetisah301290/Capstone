from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from util import *
from constants import buddhist_link
from books import Books


class Buddhist(Books):

    def __init__(self):
        super().__init__()
        self.book_name = "Buddhist"
        self.input_link =  buddhist_link

    def fetch_data(self):
        """
        :return: returns a dict by chapters implemented by each book
        """
        try:
            soup = bs(urlopen(Request(buddhist_link)).read(), 'lxml')
        except Exception as e:
            print(e)
            print("unable to fetch url")
            return
        excerpts = soup.find_all("div",class_="excerpt")
        output_dict = {}
        for chapter in excerpts:
            chapter_texts = chapter.find_all()
            text= ""
            chapter_name =""
            for i in range(0, len(chapter_texts)-2):
                if i==0:
                    chapter_name = int(re.findall(r'\d+', chapter_texts[i].get_text())[0])
                else:
                    text += chapter_texts[i].get_text()
            output_dict[chapter_name] = text
        return output_dict
