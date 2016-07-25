# Freija Descamps <freija@gmail.com> July 2016
# This is a quick tool to make the dictionary to the speech corpus
import sys
import logging
import bz2
import gensim
from gensim.corpora import Dictionary, HashDictionary, MmCorpus, WikiCorpus
import os
import wget
import json
from gensim.models import TfidfModel, LsiModel
from gensim.parsing.preprocessing import STOPWORDS
from gensim import similarities


RAWFILE = '../data/speechtext.json'
RAWIDS = '../data/speechurl.json'
MMFILE = 'speech.mm'
DICTFILE = 'speech_wordids.txt'
TDIFFILE = 'speech_tfidf.mm'
TDIFMODEL = 'speech.tdif_model'
SIMMATRIX = 'speech-lsi.index'
LSIMODEL = 'speech.lsi_model'
ARTICLEDICT = 'speech_adict.json'

DEFAULT_DICT_SIZE = 100000


def main(argv=None):
    if argv is None:
        argv = sys.argv
    print('Creating speech serialized corpus')
    # Create the speech corpus, it is inside the rawfile as a json format:
    # "id0": {"text": [" "], "url": "http://www.americanrhetoric.com/"}
    with open(RAWFILE, 'r') as f:
        speech_dict = json.load(f)
    with open(RAWIDS, 'r') as f:
        id_dict = json.load(f)
    # We also need to make sure that the article ids are saved in the correct
    # format so that the gensimple engine can understand it, like this:
    # "int": ["url", "title"],
    texts = []
    article_dict = {}
    counter = 0
    for key, value in speech_dict.items():
        texts.append([token for token in value['text']])
        article_dict[str(counter)] = [value['url'], id_dict[key]['title']]
        counter += 1
    with open(ARTICLEDICT, 'w') as f:
        json.dump(article_dict, f)
    dictionary = Dictionary(texts)
    dictionary.save_as_text(DICTFILE)
    corpus = [dictionary.doc2bow(text) for text in texts]
    MmCorpus.serialize(MMFILE, corpus)
    print('Speech serialized corpus created')
    # # Now run LSI on TDIDF
    dictionary = Dictionary.load_from_text(DICTFILE)
    mm = MmCorpus(MMFILE)
    tfidf = TfidfModel(mm, id2word=dictionary, normalize=True)
    tfidf.save(TDIFMODEL)
    MmCorpus.serialize(TDIFFILE, tfidf[mm], progress_cnt=10000)
    mm_tdif = MmCorpus(TDIFFILE)
    lsi = LsiModel(mm_tdif, id2word=dictionary, num_topics=300)
    index = similarities.MatrixSimilarity(lsi[mm_tdif])
    index.save(SIMMATRIX)
    lsi.save(LSIMODEL)
    print("LSI model and index created")


if __name__ == "__main__":
    main()
