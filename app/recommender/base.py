
class Recommender:
    recommender_id = None

    def __init__(self, corpus_name):
        # load the corpus files here
        raise NotImplementedError()

    def recommendation_for_corpus_member(article_id):
        # return a list of IDs of recommended articles
        raise NotImplementedError()

    def recommendation_for_text(text):
        # process text and return list of IDs of recommended articles
        raise NotImplementedError()
