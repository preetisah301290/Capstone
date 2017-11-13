from util import *
import pickle
from constants import pickle_path, csv_path


def cross_processing_baseline():
    f1 = open(pickle_path+"taoteching.pickle", "rb")
    f2 = open(pickle_path+"buddhist.pickle", "rb")

    taoteching_dict = pickle.load(f1)
    buddhist_dict = pickle.load(f2)
    taoteching_bag_of_words = taoteching_dict["bag_of_words"]
    buddhist_bag_of_words = buddhist_dict["bag_of_words"]
    total_counter = sum([v for v in taoteching_bag_of_words.values()]) \
                    + sum([v for v in buddhist_bag_of_words.values()])

    DTM = get_DTM_from_counter(total_counter,dicts=[taoteching_bag_of_words, buddhist_bag_of_words])
    row_labels=["Tch{}".format(k) for k in taoteching_dict['chapter_labels']] \
               + ["Bch{}".format(k) for k in buddhist_dict['chapter_labels']]
    execute_similatity_matrix(DTM,  type="tao_buddhist", label="baseline", col_row_labels=row_labels)


def find_similarChp(Chapter_index):
    """
    :param Chapter_index: 0 to 80 for TaoTeChing, 81 to rest for Buddhist
    :return:
    """
    data = np.genfromtxt(csv_path+'tao_buddhist_baselineCosSimilarity.csv',delimiter=',')
    s = range(81) if Chapter_index<81 else range(81,data.shape[0])
    arr = [i for i in s]
    print(find_closest_ChapterMatch(data,Chapter_index,skip=arr))