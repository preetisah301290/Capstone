__author__ = 'vijetasah'
import pickle

file_id = open('AllBooks.pickle','rb')
unpickled_item = pickle.load(file_id)
print(unpickled_item.get("chapter_indices"))