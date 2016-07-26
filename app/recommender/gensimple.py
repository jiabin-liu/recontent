from recommender.base import Recommender
import json
from gensim.corpora import Dictionary, HashDictionary, MmCorpus, WikiCorpus
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import smart_open, simple_preprocess
from gensim.models import LsiModel
from gensim import similarities


class GenSimple(Recommender):
    ''' A simple recommendation engine.
    It uses gensim LSI model to find similar articles inside the
    requested corpus.
    '''
    recommender_id = 'gensimple'

    def __init__(self, corpus_name):
        self.load_corpus(corpus_name)
        pass

    def load_corpus(self, corpus_name):
        ''' This is were we load the corpus files. This needs to be
        moved to a more general class initialization. (FIXME Freija)
        '''
        corpusfile = corpus_name + '.mm'
        corpusdict = corpus_name + '_wordids.txt'
        lsimodel = corpus_name + '.lsi_model'
        lsiindex = corpus_name + '-lsi.index'
        self.corpus_name = corpus_name
        self.corpus_mm = MmCorpus(corpusfile)
        self.corpus_dict = Dictionary.load_from_text(corpusdict)
        self.model = LsiModel.load(lsimodel)
        self.index = similarities.MatrixSimilarity.load(lsiindex)

    def recommendation_for_corpus_member(self, article_id):
        # return a list of IDs of recommended articles
        raise NotImplementedError()

    def recommendation_for_text(self, text):
        ''' This function is a quick toy-recommender, to be replaced with
        better things when they are available. The idea is that there
        is already a saved corpus dictionary available.
        '''
        vec_bow = self.corpus_dict.doc2bow(tokenize(text))
        vec_lsi = self.model[vec_bow]
        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return self.jsonify_rec(sims[0:6])

    def jsonify_rec(self, recommendation):
        ''' Helper function to convert the recommendation list
        to a json document. The scores will be strings as well.
        '''
        # grab the dictionary that holds the id-article translation
        # load from file:
        article_dict_file = self.corpus_name + '_adict.json'
        with open(article_dict_file, 'r') as f:
            article_dict = json.load(f)
        rec = [(article_dict[str(key)][0], str(value), article_dict[str(key)][1]) for key, value in recommendation]
        return json.dumps(rec)


def tokenize(text):
    ''' Helper function to get the tokens from a text without the
    stopwords. The stopwords are imported from gensim.
    '''
    return [token for token in simple_preprocess(text)
            if token not in STOPWORDS]
