__author__ = 'vijetasah'
import argparse
from books.Buddhism import Buddhism
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
    Buddhism,
    TaoTeChing,
    Upnishad,
    YogaSutra,
    BookProverb,
    BookEcclesiastes,
    BookEccleasiasticus,
    BookWisdom,
]

AllBooks(books_to_process).write_corpus()
