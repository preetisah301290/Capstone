import numpy as np
from sklearn.metrics.pairwise import pairwise_distances, cosine_similarity

def euclidean(DTM):
    return pairwise_distances(DTM,Y=DTM, metric="euclidean")

def manhattan(DTM):
    return pairwise_distances(DTM,Y=DTM, metric="manhattan")

def jaccard(DTM):
    tmp_DTM = np.asarray(DTM, dtype=bool)
    return pairwise_distances(tmp_DTM,Y=tmp_DTM, metric="jaccard")

def cosine(DTM):
    #eturn pairwise_distances(DTM,Y=DTM, metric="cosine")
    return cosine_similarity(DTM, DTM)

def hellinger3(p, q):
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / np.sqrt(2)

def nomalize(DTM):
    pass

def bhattacharyya(DTM):
    #provided it normalized probabilty
    DTM = np.array(DTM, dtype=float)
    DTM = (DTM.T/np.sum(DTM, axis=1)).T
    BD = -1*np.log(np.sqrt(np.dot(DTM, DTM.T)))
    return BD

similarity_matrix_dict = {
    "Cosine": cosine,
    "Jaccard": jaccard,
    "Manhattan": manhattan,
    "Euclidean": euclidean,
    #"bhattacharyya": bhattacharyya,
    #"hellinger": hellinger3
}