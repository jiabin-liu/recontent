# This is a quick tool to make the dictionary to the simple_wiki.
import sys
import logging
import bz2
import gensim
from gensim.corpora import Dictionary, HashDictionary, MmCorpus, WikiCorpus
import os
import wget
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

DEFAULT_DICT_SIZE = 100000


def main(argv=None):
    if argv is None:
        argv = sys.argv
    # Check if we have the serialized file already available,
    # if not: create it
    if not all([os.path.isfile(MMFILE),
                os.path.isfile(DICTFILE),
                os.path.isfile(TDIFFILE),
                os.path.isfile(TDIFMODEL),
                os.path.isfile(SIMMATRIX),
                os.path.isfile(LSIMODEL),
                ]):
        print('Creating simple wiki serialized corpus')
        # Download the raw file if we do not have it already
        if not os.path.isfile(WIKIFILE):
            # Get the file
            wget.download(WIKIURL)
        wiki = WikiCorpus(WIKIFILE, lemmatize=False)
        wiki.dictionary.filter_extremes(no_below=20, no_above=0.1,
                                        keep_n=DEFAULT_DICT_SIZE)
        MmCorpus.serialize(MMFILE, wiki, progress_cnt=10000)
        wiki.dictionary.save_as_text(DICTFILE)
        dictionary = Dictionary.load_from_text(DICTFILE)
        print('Simple wiki serialized corpus created')
        # initialize corpus reader and word->id mapping
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
    else:
        print('Simple wiki files available')

if __name__ == "__main__":
    main()
