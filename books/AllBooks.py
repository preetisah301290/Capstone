from util import *
from books import Books
from constants import pickle_path, csv_path, plot_path
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
            self.baseline_extend]
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
            chapter_start = chapter_start + len(d['chapter_labels'])
        DTM,unique_words = get_DTM_from_counter(total_counter,dicts=[bow_d[i] for i in self.book_names], return_words=True)
        headers = sorted(unique_words, key=unique_words.get)
        save_to_csv('{}_baseline_DTM.csv'.format(self.book_name),DTM, headers)
        self.dict["DTM"] = DTM
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
