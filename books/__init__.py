from constants import pickle_path
from gensim import models, corpora
from util import *
import pickle

class Books(object):
    def __init__(self):
        self.book_name = ""
        self.dict = None #loaded dict should be attached here
        self.input_type = "" #url # text file
        self.input_link = None
        self.input_file_path = None
        self.steps = [self.preprocess,
                      self.baseline,
                      self.log_baseline,
                      self.topic_modelling,
                      ]
        self.bias = 0.000001
        self.num_topics = 10

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
        texts = self.dict["filtered_text"]
        documents = [texts[k] for k in sorted(texts.keys())]
        all_tokens = []
        for tokens in documents:
            all_tokens.extend(tokens)
        all_tokens = Counter(all_tokens)
        unique_tokens = set(filter(lambda x: all_tokens[x] ==1,all_tokens))
        documents = [[word for word in doc if word not in unique_tokens] for doc in documents]
        # Create Dictionary.
        id2word = corpora.Dictionary(texts)
        # Creates the Bag of Word corpus.
        mm = [id2word.doc2bow(text) for text in texts]
        lda = models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=self.num_topics, \
                               update_every=1, chunksize=10000, passes=1)
        lda_corpus = lda[mm]
        lda_DTM = [[0]*self.num_topics for i in range(len(texts))]
        for doc_num, doc in enumerate(lda_corpus):
            for topic in doc:
                topic_id,score=topic
                lda_DTM[doc_num][topic_id] = score
        topics = lda.print_topics()
        topic_names = ["Topic{}".format(topic[0]) for topic in topics]
        self.dict["topics"] = topics
        self.dict["topic_names"] = topic_names
        self.dict["LDA_DTM"] = lda_DTM
        save_to_csv('{}_lda_DTM.csv'.format(self.book_name),lda_DTM, topic_names)
        execute_similatity_matrix(lda_DTM,  type=self.book_name, label="lda", col_row_labels=topic_names)
        of = open(pickle_path+self.book_name+".pickle","wb")
        pickle.dump(self.dict, of)
