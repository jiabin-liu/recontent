#!/usr/bin/env python
from flask import Flask, current_app
from flask_restful import Resource, Api, abort, reqparse
import recommender

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
            return recommender.quick_recommender(args.url, 'simple-wiki.mm', 'simple-wiki_wordids.txt')
        except recommender.URLRetrievalError:
            abort(415)
        except recommender.DocumentParsingError:
            abort(415)


api.add_resource(recommendAPI, '/api/recommend/v1.0')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
