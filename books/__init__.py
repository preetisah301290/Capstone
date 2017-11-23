from constants import pickle_path
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from util import *
import pickle

class Books(object):
    def __init__(self):
        self.book_name = ""
        self.dict = None #loaded dict should be attached here
        self.input_type = "" #url # text file
        self.input_link = None
        self.input_file_path = None
        self.steps = [self.preprocess, self.baseline, self.log_baseline, self.topic_modelling]
        self.bias = 0.000001
        self.max_df = 0.95
        self.min_df = 2
        self.no_of_features = 1000
        self.no_of_topics = 20
        self.no_of_top_topics = 10
        self.max_iter = 5
        self.learning_offset = 50.0
        self.random_state = 0

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
        self.dict["unique_words"] = headers
        save_to_csv('{}_baseline_DTM.csv'.format(self.book_name),DTM, headers)
        execute_similatity_matrix(DTM,  type=self.book_name, label="baseline", col_row_labels=row_labels)
        of = open(pickle_path+self.book_name+".pickle","wb")
        pickle.dump(self.dict, of)

    def log_baseline(self):
        if not self.dict:
            self.get_dict()

        DTM = self.dict["DTM"]
        row_labels=["ch{}".format(k) for k in self.dict['chapter_labels']]
        headers = self.dict["unique_words"]
        DTM = np.array(DTM) + self.bias
        DTM = np.log(DTM)
        DTM[DTM<0] = 0.0
        save_to_csv('{}_baseline_log_DTM.csv'.format(self.book_name),DTM, headers)
        self.dict["Log_DTM"] = DTM
        execute_similatity_matrix(DTM,  type=self.book_name, label="baseline_log", col_row_labels=row_labels)
        of = open(pickle_path+self.book_name+".pickle","wb")
        pickle.dump(self.dict, of)

    def topic_modelling(self):
        if not self.dict:
            self.get_dict()
        """
        raw_texts = self.dict["raw_text"]
        documents  = [raw_texts[k] for k in sorted(raw_texts.keys())]
        tf_vectorizer = CountVectorizer(max_df=self.max_df, min_df=self.min_df,
                                        max_features=self.no_of_features, stop_words='english')
        tf = tf_vectorizer.fit_transform(documents)
        tf_feature_names = tf_vectorizer.get_feature_names()
        lda = LatentDirichletAllocation(n_topics=self.no_of_topics,
                                        max_iter=self.max_iter, learning_method='online',
                                        learning_offset=self.learning_offset,random_state=self.random_state).fit(tf)
        """