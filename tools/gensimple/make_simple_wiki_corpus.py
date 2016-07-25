# Freija Descamps <freija@gmail.com> July 2016
# This is a quick tool to make the dictionary to the simple_wiki.
# It requires a tweaked version of gensim
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


def tokenize(text):
    return [token for token in simple_preprocess(text) if token not in STOPWORDS]


WIKIURL = 'https://dumps.wikimedia.org/simplewiki/20160701/simplewiki-20160701-pages-articles-multistream.xml.bz2'
WIKIFILE = 'simplewiki-20160701-pages-articles-multistream.xml.bz2'
MMFILE = 'simple-wiki.mm'
DICTFILE = 'simple-wiki_wordids.txt'
TDIFFILE = 'simple-wiki_tfidf.mm'
TDIFMODEL = 'simple-wiki.tdif_model'
SIMMATRIX = 'simple-wiki-lsi.index'
LSIMODEL = 'simple-wiki.lsi_model'
ARTICLEDICT = 'simple-wiki_adict.json'

DEFAULT_DICT_SIZE = 100000


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Creating simple wiki serialized corpus')
    # Download the raw file if we do not have it already
    if not os.path.isfile(WIKIFILE):
        # Get the file
        wget.download(WIKIURL)
    wiki = WikiCorpus(WIKIFILE, lemmatize=False)
    i = 0
    article_dict = {}
    for text in wiki.get_texts(meta=True):
        url_string = 'simple.wikipedia.org/wiki/?curid={}'
        article_dict[i] = (url_string.format(text[0]), text[1])
        i += 1
    with open(ARTICLEDICT, 'w') as f:
        json.dump(article_dict, f)
    wiki.dictionary.filter_extremes(no_below=20, no_above=0.1,
                                    keep_n=DEFAULT_DICT_SIZE)
    MmCorpus.serialize(MMFILE, wiki, progress_cnt=10000, )
    wiki.dictionary.save_as_text(DICTFILE)
    print('Simple wiki serialized corpus created')
    # Now run LSI
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
