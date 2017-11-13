import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

csv_path = "DataCSV/"
pickle_path = "DataPickle/"
plot_path = "DataPlots/"
buddhist_link = "https://www.accesstoinsight.org/lib/study/truths.html"
taoteching_input_file = "TaoTeChing.txt"
stop_words = set(stopwords.words('english'))
