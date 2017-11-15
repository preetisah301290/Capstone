import argparse
from books.Buddhist import Buddhist
from books.Taoteching import TaoTeChing
from books.Upnishad import Upnishad
from books.YogaSutra import YogaSutra
from books.BookProverb import BookProverb
from books.BookEcclesiastes import BookEcclesiastes
from books.BookEccleasiasticus import BookEccleasiasticus
from books.BookWisdom import BookWisdom
from books.AllBooks import AllBooks

from util import *

books_to_process = [
    #Buddhist,
    #TaoTeChing,
    #Upnishad, #161 chapters need to read properly
    YogaSutra, #Not Working
    #BookProverb, #Too Big DTM 942 chapters retification Needed
    #BookEcclesiastes, #Too Big DTM 224 chapters retification Needed
    #BookEccleasiasticus, #Nope this is 1592 chapters
    #BookWisdom, #Nope 440 chapters
]


def project_run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="starting step")
    args = parser.parse_args()
    step = 0
    if not args.step:
        step = int(step)
    for b in books_to_process:
        book = b()
        print("processing for {}".format(book.book_name))
        for i in range(step, len(book.steps)):
            book.steps[i]()

    for func in AllBooks(books_to_process).steps:
        func()



if __name__=='__main__':
    project_run()


