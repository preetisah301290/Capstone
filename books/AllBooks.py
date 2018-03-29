from util import *
from books import Books
from constants import pickle_path, csv_path, plot_path
from gensim import models, corpora
import itertools
import pickle
from similarity import similarity_matrix_dict
import csv


class AllBooks(Books):
    def __init__(self, all_books):
        super().__init__()
        self.book_name = "AllBooks"
        self.steps = [
            self.baseline,
            self.baseline_extend,
            self.log_baseline,
            self.log_baseline_extend,
            self.topic_modelling,
            self.topic_modelling_extend,
        ]
        self.all_books = all_books
        self.book_names = []
        self.dict = {}
        self.num_topics = 26



    def write_corpus(self):

        f= open("Complete_data","w+")
        for i,b in enumerate(self.all_books):
            book =b()
            d = book.get_dict()
            raw_text=d['raw_text']
            for k in sorted(raw_text.keys()):
                text = raw_text[k]
                text = text.replace("\n"," ")
                f.write(str(i)+"."+str(k)+"\n"+text+"\n")
        f.close()

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
            chapter_start = chapter_start + len(d['chapter_labels'])
        DTM,unique_words = get_DTM_from_counter(total_counter,dicts=[bow_d[i] for i in self.book_names], return_words=True)
        headers = sorted(unique_words, key=unique_words.get)
        save_to_csv('{}_baseline_DTM.csv'.format(self.book_name),DTM, headers)
        self.dict["DTM"] = DTM
        self.dict["unique_words"] = headers
        self.dict["row_labels"] = row_labels
        self.dict["bag_of_words"] = total_counter
        self.dict["chapter_indices"] = chapter_indices
        self.dict["books"] = self.all_books
        of = open(pickle_path+self.book_name+".pickle","wb")
        pickle.dump(self.dict, of)
        execute_similatity_matrix(DTM,  type=self.book_name, label="baseline", col_row_labels=row_labels)

    def baseline_extend(self):
        print("processing for {} and extend baseline".format(self.book_name))
        if not self.dict:
            self.dict = self.get_dict()

        l = len(self.dict["books"])
        books_header = [b().book_name for b in self.dict["books"]]
        for k,v in similarity_matrix_dict.items():
            print("processing for {} and extend baseline and {}".format(self.book_name, k))
            data = np.genfromtxt("{}{}_baseline_{}.csv".format(csv_path, self.book_name,k),
                                 dtype=float, delimiter=',', skip_header=1)

            avg_dist_sim = [[0]*l for i in range(l)]
            median_dist_sim = [[0]*l for i in range(l)]
            min_dist_sim = [["0"]*l for i in range(l)]
            max_dist_sim = [["0"]*l for i in range(l)]
            for i, j in itertools.combinations_with_replacement(range(l), 2):
                x1,x2 = self.dict["chapter_indices"][books_header[i]]
                y1,y2 = self.dict["chapter_indices"][books_header[j]]
                n_data=data[x1:x2+1, y1:y2+1]
                avg_dist_sim[i][j] = avg_dist_sim[j][i] = np.mean(n_data)
                median_dist_sim[i][j] = median_dist_sim[j][i] = np.median(n_data)
                max_dist_sim[i][j] = max_dist_sim[j][i] = "{}|{}|{}".format(
                        np.max(n_data), *np.unravel_index(n_data.argmax(),n_data.shape))
                min_dist_sim[i][j] = min_dist_sim[j][i] = "{}|{}|{}".format(
                        np.min(n_data), *np.unravel_index(n_data.argmin(),n_data.shape))

            save_to_csv('{}_basline_avg_{}.csv'.format(self.book_name,k),avg_dist_sim, books_header)
            save_to_csv('{}_basline_median_{}.csv'.format(self.book_name,k),median_dist_sim, books_header)
            save_to_csv('{}_basline_max_{}.csv'.format(self.book_name,k),max_dist_sim, books_header, fmt_type='%s')
            save_to_csv('{}_basline_min_{}.csv'.format(self.book_name,k),min_dist_sim, books_header, fmt_type='%s')

            plot_heatmap(np.array(median_dist_sim), books_header, books_header,
                         '{}_basline_median_{}.png'.format(self.book_name,k))
            plot_heatmap(np.array(avg_dist_sim), books_header, books_header,
                         '{}_basline_avg_{}.png'.format(self.book_name,k))

            min_l = [[float(y.split('|')[0]) for y in x] for x in min_dist_sim]
            plot_heatmap(np.array(min_l), books_header, books_header,
                         '{}_basline_min_{}.png'.format(self.book_name,k))
            max_l = [[float(y.split('|')[0]) for y in x] for x in max_dist_sim]
            plot_heatmap(np.array(max_l), books_header, books_header,
                         '{}_basline_max_{}.png'.format(self.book_name,k))

    def log_baseline(self):
        print("processing for {} and baseline log".format(self.book_name))
        if not self.dict:
            self.dict = self.get_dict()

        DTM = self.dict["DTM"]
        headers = self.dict["unique_words"]
        row_labels = self.dict["row_labels"]
        DTM = np.array(DTM) + self.bias
        DTM = np.log(DTM)
        DTM[DTM<0] = 0.0
        self.dict["Log_DTM"] = DTM
        save_to_csv('{}_baseline_log_DTM.csv'.format(self.book_name),DTM, headers)
        execute_similatity_matrix(DTM,  type=self.book_name, label="baseline_log", col_row_labels=row_labels)
        of = open(pickle_path+self.book_name+".pickle","wb")
        pickle.dump(self.dict, of)

    def log_baseline_extend(self):
        print("processing for {} and  extend baseline log".format(self.book_name))
        if not self.dict:
            self.dict = self.get_dict()

        l = len(self.dict["books"])
        books_header = [b().book_name for b in self.dict["books"]]
        for k,v in similarity_matrix_dict.items():
            print("processing for {} and extend baseline log and {}".format(self.book_name, k))
            data = np.genfromtxt("{}{}_baseline_log_{}.csv".format(csv_path, self.book_name,k),
                                 dtype=float, delimiter=',', skip_header=1)

            avg_dist_sim = [[0]*l for i in range(l)]
            median_dist_sim = [[0]*l for i in range(l)]
            min_dist_sim = [["0"]*l for i in range(l)]
            max_dist_sim = [["0"]*l for i in range(l)]
            for i, j in itertools.combinations_with_replacement(range(l), 2):
                x1,x2 = self.dict["chapter_indices"][books_header[i]]
                y1,y2 = self.dict["chapter_indices"][books_header[j]]
                n_data=data[x1:x2+1, y1:y2+1]
                avg_dist_sim[i][j] = avg_dist_sim[j][i] = np.mean(n_data)
                median_dist_sim[i][j] = median_dist_sim[j][i] = np.median(n_data)
                max_dist_sim[i][j] = max_dist_sim[j][i] = "{}|{}|{}".format(
                        np.max(n_data), *np.unravel_index(n_data.argmax(),n_data.shape))
                min_dist_sim[i][j] = min_dist_sim[j][i] = "{}|{}|{}".format(
                        np.min(n_data), *np.unravel_index(n_data.argmin(),n_data.shape))

            save_to_csv('{}_basline_log_avg_{}.csv'.format(self.book_name,k),avg_dist_sim, books_header)
            save_to_csv('{}_basline_log_median_{}.csv'.format(self.book_name,k),median_dist_sim, books_header)
            save_to_csv('{}_basline_log_max_{}.csv'.format(self.book_name,k),max_dist_sim, books_header, fmt_type='%s')
            save_to_csv('{}_basline_log_min_{}.csv'.format(self.book_name,k),min_dist_sim, books_header, fmt_type='%s')

            plot_heatmap(np.array(median_dist_sim), books_header, books_header,
                         '{}_basline_log_median_{}.png'.format(self.book_name,k))
            plot_heatmap(np.array(avg_dist_sim), books_header, books_header,
                         '{}_basline_log_avg_{}.png'.format(self.book_name,k))

            min_l = [[float(y.split('|')[0]) for y in x] for x in min_dist_sim]
            plot_heatmap(np.array(min_l), books_header, books_header,
                         '{}_basline_log_min_{}.png'.format(self.book_name,k))
            max_l = [[float(y.split('|')[0]) for y in x] for x in max_dist_sim]
            plot_heatmap(np.array(max_l), books_header, books_header,
                         '{}_basline_log_max_{}.png'.format(self.book_name,k))

    def topic_modelling(self):
        print("processing for {} and topic_modelling".format(self.book_name))
        if not self.dict:
            self.get_dict()

        texts = []
        for b in self.all_books:
            book =b()
            d = book.get_dict()
            self.book_names.append(book.book_name)
            filter_text = d["filtered_text"]
            texts.extend([filter_text[k] for k in sorted(filter_text.keys())])
        all_tokens = []
        for tokens in texts:
            all_tokens.extend(tokens)
        all_tokens = Counter(all_tokens)
        unique_tokens = set(filter(lambda x: all_tokens[x] ==1,all_tokens))
        documents = [[word for word in doc if word not in unique_tokens] for doc in texts]
        chapter_indices = self.dict["chapter_indices"]
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

        words_each_topic = dict(topics)
        for k,v in words_each_topic.items():
            x=v.split("+")
            y=[z.split("*")[1].replace("\"","") for z in x]
            words_each_topic[k] = y
            print(k,y)
        topic_names = ["Topic{}".format(i) for i in range(self.num_topics)]
        print("topic names :",topic_names)
        self.dict["topics"] = topics
        self.dict["topic_names"] = topic_names
        self.dict["LDA_DTM"] = lda_DTM
        row_labels = self.dict["row_labels"]
        save_to_csv('{}_lda_DTM.csv'.format(self.book_name),lda_DTM, topic_names)
        execute_similatity_matrix(lda_DTM,  type=self.book_name, label="lda", col_row_labels=row_labels)
        of = open(pickle_path+self.book_name+".pickle","wb")
        pickle.dump(self.dict, of)


    def topic_modelling_extend(self):
        print("processing for {} and  extend topic modeling log".format(self.book_name))
        if not self.dict:
            self.dict = self.get_dict()
        l = len(self.dict["books"])
        books_header = [b().book_name for b in self.dict["books"]]
        for k,v in similarity_matrix_dict.items():
            print("processing for {} and extend topic modelling and {}".format(self.book_name, k))
            data = np.genfromtxt("{}{}_lda_{}.csv".format(csv_path, self.book_name,k),
                                 dtype=float, delimiter=',', skip_header=1)

            avg_dist_sim = [[0]*l for i in range(l)]
            median_dist_sim = [[0]*l for i in range(l)]
            min_dist_sim = [["0"]*l for i in range(l)]
            max_dist_sim = [["0"]*l for i in range(l)]
            for i, j in itertools.combinations_with_replacement(range(l), 2):
                x1,x2 = self.dict["chapter_indices"][books_header[i]]
                y1,y2 = self.dict["chapter_indices"][books_header[j]]
                n_data=data[x1:x2+1, y1:y2+1]
                avg_dist_sim[i][j] = avg_dist_sim[j][i] = np.mean(n_data)
                median_dist_sim[i][j] = median_dist_sim[j][i] = np.median(n_data)
                max_dist_sim[i][j] = max_dist_sim[j][i] = "{}|{}|{}".format(
                        np.max(n_data), *np.unravel_index(n_data.argmax(),n_data.shape))
                min_dist_sim[i][j] = min_dist_sim[j][i] = "{}|{}|{}".format(
                        np.min(n_data), *np.unravel_index(n_data.argmin(),n_data.shape))

            save_to_csv('{}_lda_avg_{}.csv'.format(self.book_name,k),avg_dist_sim, books_header)
            save_to_csv('{}_lda_median_{}.csv'.format(self.book_name,k),median_dist_sim, books_header)
            save_to_csv('{}_lda_max_{}.csv'.format(self.book_name,k),max_dist_sim, books_header, fmt_type='%s')
            save_to_csv('{}_lda_min_{}.csv'.format(self.book_name,k),min_dist_sim, books_header, fmt_type='%s')

            plot_heatmap(np.array(median_dist_sim), books_header, books_header,
                         '{}_lda_median_{}.png'.format(self.book_name,k))
            plot_heatmap(np.array(avg_dist_sim), books_header, books_header,
                         '{}_lda_avg_{}.png'.format(self.book_name,k))

            min_l = [[float(y.split('|')[0]) for y in x] for x in min_dist_sim]
            plot_heatmap(np.array(min_l), books_header, books_header,
                         '{}_lda_min_{}.png'.format(self.book_name,k))
            max_l = [[float(y.split('|')[0]) for y in x] for x in max_dist_sim]
            plot_heatmap(np.array(max_l), books_header, books_header,
                         '{}_lda_max_{}.png'.format(self.book_name,k))