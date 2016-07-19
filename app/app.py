#!/usr/bin/env python
from flask import Flask, current_app
from flask_restful import Resource, Api, abort, reqparse
import parser
from recommender import gensimple

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return "Content recommendation rocks!"


class recommendAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, help='url for document that\
                                                          requires content\
                                                          recommendation')
        super(recommendAPI, self).__init__()

    def get(self):
        # For now, get the argument and run an
        # argument checker on it
        args = self.reqparse.parse_args()
        try:
            text_from_url = parser.get_document(args.url)
        except parser.URLRetrievalError:
            abort(415)
        except parser.DocumentParsingError:
            abort(415)
        corpus_name = 'simple-wiki'
        this_recommender = gensimple.GenSimple(corpus_name)
        recommendation = this_recommender.recommendation_for_text(text_from_url)
        # This currenly just returns a BOW for the article
        return recommendation

api.add_resource(recommendAPI, '/api/recommend/v1.0')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
