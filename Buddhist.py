from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from util import *
from constants import buddhist_link, pickle_path, csv_path
import pickle


def buddhist_preprocess():
    try:
        soup = bs(urlopen(Request(buddhist_link)).read())
    except Exception as e:
        print(e)
        print("unable to fetch url")
        return

    excerpts = soup.find_all("div",class_="excerpt")
    output_dict = {}
    for chapter in excerpts:
        chapter_texts = chapter.find_all()
        text= ""
        chapter_name =""
        for i in range(0, len(chapter_texts)-2):
            if i==0:
                chapter_name = int(re.findall(r'\d+', chapter_texts[i].get_text())[0])
            else:
                text += chapter_texts[i].get_text()
        output_dict[chapter_name] = text
    filtered_dict = dict()
    for k,v in output_dict.items():
        filtered_dict[k] = clean_data(v)
    chapter_labels=[k for k in sorted(output_dict.keys())]
    final_dict = dict()
    final_dict['raw_text'] = output_dict
    final_dict['filtered_text'] = filtered_dict
    final_dict['chapter_labels'] = chapter_labels
    of = open(pickle_path+"buddhist.pickle","wb")
    pickle.dump(final_dict, of)


def buddhist_baseline():
    f = open(pickle_path+"buddhist.pickle","rb")
    input_dict = pickle.load(f)
    f.close()
    #bag of words by chapter
    bag_of_words = get_bag_of_words_by_chapter(input_dict['filtered_text'])
    input_dict["bag_of_words"] = bag_of_words
    total_counter = sum([v for v in bag_of_words.values()])
    DTM = get_DTM_from_counter(total_counter,dicts=[bag_of_words])
    input_dict["DTM"] = DTM
    row_labels=["ch{}".format(k) for k in input_dict['chapter_labels']]
    execute_similatity_matrix(DTM,  type="buddhist", label="baseline", col_row_labels=row_labels)
    of = open(pickle_path+"buddhist.pickle","wb")
    pickle.dump(input_dict, of)


# findind the closest matching chapter within buddhism
def buddhist_find_similarChp(Chapter_index):
    data = np.genfromtxt(csv_path+'buddhist_baselineCosineSimilarity.csv',delimiter=',')
    print(find_closest_ChapterMatch(data,Chapter_index))
