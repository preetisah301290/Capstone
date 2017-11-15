import sys
import os
import pickle
import argparse
from Buddhist import *
from TaoTeChing import *
from BookEccleasiasticus import*
from BookWisdom import *
from BookEcclesiastes import *
from BookProverb import *
from cross_processing import *
from YogaSutra import *
from Upanishad import *
from util import *

process_step = {
    "budhist":[buddhist_preprocess, buddhist_baseline],
    "chiense":[taoteching_preprocess, taoteching_baseline],
    "upnishad":[upnishad_preprocess, upnishad_baseline],
    "yogasutra":[yogasutra_preprocess, yogasutra_baseline],
    "BookProverb":[BookProverb_preprocess,BookProverb_baseline],
    "BookEcclesiastes":[BookEcclesiastes_preprocess,BookEcclesiastes_baseline],
    "BookEccleasiasticus" :[BookEccleasiasticus_preprocess,BookEccleasiasticus_baseline],
    "BookWisdom":[BookWisdom_preprocess,BookWisdom_baseline]
    }

#cross_processing_step = []
cross_processing_step = [cross_processing_baseline]
def project_run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="starting step")
    args = parser.parse_args()
    step = 0
    if not args.step:
        step = int(step)
    for k,v in process_step.items():
        print("processing for {}".format(k))
        for i in range(step, len(v)):
            v[i]()

    for func in cross_processing_step:
        func()


    # finding most similar chapters within buddhism based on chapter index provided
    #buddhist_find_similarChp(2)

    # finding most similar chapters within Tao-ism
    #toa_find_similarChp(1)

    # finding most similar chapters from Taoism in buddhism and vice versa
    #find_similarChp(42)



if __name__=='__main__':
    project_run()


