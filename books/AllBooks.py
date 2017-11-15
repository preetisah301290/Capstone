from util import *
from books import Books
from constants import pickle_path
import pickle

class AllBooks(Books):
    def __init__(self, all_books):
        super().__init__()
        self.book_name = "AllBooks"
        self.steps = [self.baseline,]
        self.all_books = all_books
        self.book_names = []
        self.dict = {}

    def baseline(self):
        total_counter = Counter()
        self.book_names = []
        bow_d = {}
        row_labels = []
        chapter_start = 0
        chapter_indices = {}
        for b in self.all_books:
            book =b()
            d = book.get_dict()
            self.book_names.append(book.book_name)
            bow = d["bag_of_words"]
            total_counter += sum([v for v in bow.values()])
            bow_d[book.book_name] = bow
            row_labels.extend(["{}_ch{}".format(book.book_name, k) for k in d['chapter_labels']])
            chapter_indices[book.book_name] = (chapter_start, chapter_start+len(d['chapter_labels'])-1)
            chapter_start = chapter_start+len(d['chapter_labels'])
        DTM = get_DTM_from_counter(total_counter,dicts=[bow_d[i] for i in self.book_names])
        self.dict["DTM"] = DTM
        self.dict["bag_of_words"] = total_counter
        self.dict["chapter_indices"] = chapter_indices
        self.dict["books"] = self.all_books
        of = open(pickle_path+self.book_name+".pickle","wb")
        pickle.dump(self.dict, of)
        execute_similatity_matrix(DTM,  type=self.book_name, label="baseline", col_row_labels=row_labels)
