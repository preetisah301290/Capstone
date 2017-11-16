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

def hellinger3(DTM):
    DTM = nomalize(DTM)
    return euclidean(DTM) / np.sqrt(2)

def nomalize(DTM):
    pass

def bhattacharyya(DTM):
    #provided it normalized probabilty
    DTM = np.array(DTM, dtype=float)
    DTM = (DTM.T/np.sum(DTM, axis=1)).T
    BD = -1*np.log(np.sqrt(np.dot(DTM, DTM.T)))
    return BD

similarity_matrix_dict = {
    "Cosine_Similarity": cosine,
    "Jaccard_Distance": jaccard,
    "Manhattan_Distance": manhattan,
    "Euclidean_Distance": euclidean,
    #"bhattacharyya_Distance": bhattacharyya,
    #"hellinger_Distance": hellinger3
}