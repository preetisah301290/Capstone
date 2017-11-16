from constants import pickle_path
from util import *
import pickle

class Books(object):
    def __init__(self):
        self.book_name = ""
        self.dict = None #loaded dict should be attached here
        self.input_type = "" #url # text file
        self.input_link = None
        self.input_file_path = None
        self.steps = [self.preprocess, self.baseline,]

    def fetch_data(self):
        """
        :return: returns a dict by chapters implemented by each book
        """
        return {}

    def get_dict(self):
        if self.dict:
            return self.dict
        f = open(pickle_path+self.book_name+".pickle","rb")
        self.dict = pickle.load(f)
        f.close()
        return self.dict

    def preprocess(self):
        output_dict = self.fetch_data()
        filtered_dict = dict()
        for k,v in output_dict.items():
            filtered_dict[k] = clean_data(v)
        chapter_labels=[k for k in sorted(output_dict.keys())]
        final_dict = dict()
        final_dict['raw_text'] = output_dict
        final_dict['filtered_text'] = filtered_dict
        final_dict['chapter_labels'] = chapter_labels
        self.dict =final_dict
        of = open(pickle_path+self.book_name+".pickle","wb")
        pickle.dump(final_dict, of)

    def baseline(self):
        if not self.dict:
            self.get_dict()
        #bag of words by chapter
        bag_of_words = get_bag_of_words_by_chapter(self.dict['filtered_text'])
        self.dict["bag_of_words"] = bag_of_words
        total_counter = sum([v for v in bag_of_words.values()])
        DTM, unique_words = get_DTM_from_counter(total_counter,dicts=[bag_of_words], return_words=True)
        self.dict["DTM"] = DTM
        row_labels=["ch{}".format(k) for k in self.dict['chapter_labels']]
        headers = sorted(unique_words, key=unique_words.get)
        save_to_csv('{}_baseline_DTM.csv'.format(self.book_name),DTM, headers)
        execute_similatity_matrix(DTM,  type=self.book_name, label="baseline", col_row_labels=row_labels)
        of = open(pickle_path+self.book_name+".pickle","wb")
        pickle.dump(self.dict, of)
