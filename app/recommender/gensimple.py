from recommender.base import Recommender
import gensim
import pandas
from gensim.corpora import Dictionary, HashDictionary, MmCorpus, WikiCorpus
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import smart_open, simple_preprocess


class GenSimple(Recommender):
    recommender_id = 'gensimple'

    def __init__(self, corpus_name):
        self.load_corpus(corpus_name)
        pass

    def load_corpus(self, corpus_name):
        # load the corpus here
        corpusfile = corpus_name + '.mm'
        corpusdict = corpus_name + '_wordids.txt'
        self.corpus_mm = MmCorpus(corpusfile)
        self.corpus_dict = HashDictionary(corpusdict)

    def recommendation_for_corpus_member(self, article_id):
        # return a list of IDs of recommended articles
        raise NotImplementedError()

    def recommendation_for_text(self, text):
        ''' This function is a quick toy-recommender, to be replaced with
        better things when they are available. The idea is that there
        is already a saved corpus dictionary available, which is passed
        on as an argument. The corpusfile is expected to be an mmcorpus.
        '''
        bow_vector = self.corpus_dict.doc2bow(tokenize(text))
        # Insert some recommender code here
        # for now, just return the bow_vector of the text
        return bow_vector


def tokenize(text):
    ''' Helper function to get the tokens from a text without the
    stopwords. The stopwords are imported from gensim.
    '''
    return [token for token in simple_preprocess(text)
            if token not in STOPWORDS]
