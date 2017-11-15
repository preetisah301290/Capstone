from pylab import *
import numpy as np
from nltk import word_tokenize, sent_tokenize
from constants import stop_words
import re
from collections import Counter
from similarity import similarity_matrix_dict

def clean_data(data):
    sents = sent_tokenize(data)
    words = list()
    for sent in sents:
        words.extend(word_tokenize(sent))
    words = [w.lower() for w in words if not w.lower() in stop_words]
    words = [re.sub(r"[^a-zA-Z]+", '', w) for w in words]
    words = [w for w in words if w!='']
    return words


def get_bag_of_words_by_chapter(d):
    return {k:Counter(v) for k,v in d.items()}


def plot_heatmap(data, colnames, rownames, plot_filename):
    fig, axis = plt.subplots()
    heatmap = axis.pcolor(data, cmap=plt.cm.Blues)
    axis.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
    axis.set_xticks(np.arange(data.shape[1])+0.5, minor=False)

    axis.invert_yaxis()

    axis.set_yticklabels(rownames, minor=False)
    axis.set_xticklabels(colnames, minor=False)

    plt.colorbar(heatmap)

    plt.savefig(plot_filename)
    #show()


def get_DTM_from_counter(total_counter, dicts=list()):
    unique_words_dict = dict({(k,i) for i,k in enumerate(total_counter)})
    DTM = [[0]*len(unique_words_dict) for _ in range(sum([len(d) for d in dicts]))]
    i = 0
    for output_dict in dicts:
        for ch in sorted(output_dict.keys()):
            v = output_dict[ch]
            for word, count in v.items():
                DTM[i][unique_words_dict[word]] = count
            i+=1
    return DTM


def find_closest_ChapterMatch(DTM, Chapter_colname, skip=[]):
    Chapter_col = DTM[Chapter_colname]
    max_value = -Infinity
    max_index= None
    for i, v in enumerate(Chapter_col):
        if i == Chapter_colname  or i in skip:
            continue
        else:
            if v> max_value:
                max_value = v
                max_index = i

    return max_value,max_index



def execute_similatity_matrix(DTM, type="all", label="baseline", col_row_labels=[]):
    print("Executing Similarity for {} and {}".format(type, label))
    for k, func_sim in  similarity_matrix_dict.items():
        sm = np.array(func_sim(DTM))
        headers = ','.join(col_row_labels)
        np.savetxt('DataCSV/{}_{}{}Similarity.csv'.format(type, label,k), sm, fmt='%f', delimiter=',', header=headers)
        plot_heatmap(sm, col_row_labels, col_row_labels,'DataPlots/{}_{}{}Similarity.png'.format(type,label,k))



