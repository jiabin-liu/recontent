#!/usr/bin/env python
from flask import Flask, current_app
from flask_restful import Resource, Api, abort, reqparse
import recommender

app = Flask(__name__)
api = Api(app)


# For now, let's keep a list of the requested urls here as a dictionary
# We will want to move this to a presistent database (SQLite?)
# This is still just test-data
urls = {
    'url_id1': {'url':'http://www.symmetrymagazine.org/article/scientists-salvage-insights-from-lost-satellite',
                'arxiv_recommendation': [('https://arxiv.org/abs/astro-ph/0201381', 0.925),
                                         ('https://arxiv.org/abs/astro-ph/0201361', 0.880),
                                         ('https://arxiv.org/abs/astro-ph/0201336', 0.231)
                                         ]
                },
}


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
        return [recommender.url_exists(args.url),
                recommender.url_valid(args.url),
                recommender.url_html(args.url)]


api.add_resource(recommendAPI, '/api/recommend/v1.0')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
