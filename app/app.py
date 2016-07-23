#!/usr/bin/env python
import parser
import random
from flask import Flask, current_app, jsonify
from flask_restful import Resource, Api, abort, reqparse
from recommender.base import Recommender
# Import the recommendation engines here to register them
from recommender.gensimple import GenSimple

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return "Content recommendation rocks!"


class recommendAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url',
                                   type=str,
                                   help='url for document that requires content recommendation')
        # Prepare the list of available engines. This will find all engines
        # that are imported explicitly
        self.engine_classes = Recommender.__subclasses__()
        self.recommenders = dict()
        super(recommendAPI, self).__init__()

    def get(self, corpus_name):
        # Get the argument: a URL as a string
        args = self.reqparse.parse_args()
        # Check the input URL
        try:
            text_from_url = parser.get_document(args.url)
        except parser.URLRetrievalError:
            abort(415)
        except parser.DocumentParsingError:
            abort(415)
        # Now, pick a recommendation engine. For now, this is done at random
        random_recommender = random.choice(self.engine_classes)
        if (random_recommender, corpus_name) not in self.recommenders:
            self.recommenders[(random_recommender, corpus_name)] = random_recommender(corpus_name)
        this_recommender = self.recommenders[(random_recommender, corpus_name)]
        recommendation = this_recommender.recommendation_for_text(text_from_url)
        return recommendation

api.add_resource(recommendAPI, '/api/recommend/v1.0/<corpus_name>')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
