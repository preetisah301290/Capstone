from util import *
from constants import taoteching_input_file, pickle_path, csv_path, roman_numeral,upnishad_studyline, upnishad_file
import pickle
from collections import Counter

def upnishad_preprocess():
    req = open(upnishad_file)
    output_dict = {}
    lines = [line for line in req.readlines()]
    ch = 1
    for i,j in upnishad_studyline:
        text=""
        for line in lines[i:j]:
            if line.strip() in roman_numeral:
                if text!="":
                    output_dict[ch]=text
                    ch+=1
                text=""
            else:
                text+=line
        if text!="":
            output_dict[ch] = text

    filtered_dict = dict()
    for k,v in output_dict.items():
        filtered_dict[k] = clean_data(v)
    chapter_labels=[k for k in sorted(output_dict.keys())]
    final_dict = dict()
    final_dict['raw_text'] = output_dict
    final_dict['filtered_text'] = filtered_dict
    final_dict['chapter_labels'] =chapter_labels
    of = open(pickle_path+"upnishad.pickle", "wb")
    pickle.dump(final_dict, of)


def upnishad_baseline():
    f = open(pickle_path+"upnishad.pickle","rb")
    input_dict = pickle.load(f)
    f.close()
    #bag of words by chapter
    bag_of_words = get_bag_of_words_by_chapter(input_dict['filtered_text'])
    input_dict["bag_of_words"] = bag_of_words
    total_counter = sum([v for v in bag_of_words.values()])
    DTM = get_DTM_from_counter(total_counter,dicts=[bag_of_words])
    input_dict["DTM"] = DTM
    row_labels=["ch{}".format(k) for k in input_dict['chapter_labels']]
    execute_similatity_matrix(DTM,  type="upnishad", label="baseline", col_row_labels=row_labels)

    of = open(pickle_path+"upnishad.pickle","wb")
    pickle.dump(input_dict, of)

def upnishad_find_similarChp(Chapter_index):
    data = np.genfromtxt(csv_path+'upnishad_baselineCosineSimilarity.csv',delimiter=',')
    print(find_closest_ChapterMatch(data,Chapter_index))