# This is a quick tool to make the dictionary to the simple_wiki.
import sys
import logging
import bz2
import gensim
from gensim.corpora import Dictionary, HashDictionary, MmCorpus, WikiCorpus
import os
import wget

WIKIURL = 'https://dumps.wikimedia.org/simplewiki/20160701/simplewiki-20160701-pages-articles-multistream.xml.bz2'
WIKIFILE = 'simplewiki-20160701-pages-articles-multistream.xml.bz2'
MMFILE = 'simple-wiki.mm'
DICTFILE = 'simple-wiki_wordids.txt'

DEFAULT_DICT_SIZE = 100000


def main(argv=None):
    if argv is None:
        argv = sys.argv
    # Check if we have the serialized file already available,
    # if not: create it
    if not all([os.path.isfile(MMFILE), os.path.isfile(DICTFILE)]):
        print('Creating small wiki serialized corpus')
        # Download the raw file if we do not have it already
        if not os.path.isfile(WIKIFILE):
            # Get the file
            wget.download(WIKIURL)
        dictionary = HashDictionary(id_range=DEFAULT_DICT_SIZE, debug=True)
        dictionary.allow_update = True
        wiki = WikiCorpus(WIKIFILE, lemmatize=False, dictionary=dictionary)
        MmCorpus.serialize(MMFILE, wiki, progress_cnt=10000)
        dictionary.filter_extremes(no_below=20, no_above=0.1,
                                   keep_n=DEFAULT_DICT_SIZE)
        dictionary.save_as_text(DICTFILE)
        # wiki.save('small-wiki_corpus.pkl.bz2')
        print('Simple wiki serialized corpus created')
        print(dictionary)
    else:
        print('Simple wiki files available')

if __name__ == "__main__":
    main()
