#!/usr/bin/env python
import parser
import random
import flask
import json
import numpy as np
from flask import Flask, current_app, jsonify, request, render_template, redirect
from flask_restful import Resource, Api, abort, reqparse
from recommender.base import Recommender
# Import the recommendation engines here to register them
from recommender.gensimple import GenSimple
import time

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import recordclicks

import clickstats

app = Flask(__name__)
api = Api(app)

client = MongoClient()
db = client.clickdb
clicks = db.clicks

@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/tryitout')
def tryitout():
    return flask.render_template("enterurl.html")

@app.route('/tryitout', methods = ['POST'])
def show_rec():

    inputurl = request.form['inputurl']

    userecAPI = recommendAPI(recommenders)
    userecAPI.reqparse.remove_argument('url')
    userecAPI.reqparse.add_argument('url', type = str, default = inputurl)

    resultdata = userecAPI.get('speech')

    return render_template('sitelist.html', resultdata = resultdata)


@app.route('/documentation')
def documentation():
    return flask.render_template("documentation.html")


@app.route('/contact')
def contact():
    return flask.render_template("contact.html")


@app.route('/dashboard')
def dashboard():
    """
    This is the dashboard that displays some interesting
    stats for our recommendation API service.
    """
    data_summary = clickstats.getdatasummary()
    return flask.render_template("dashboard.html",
                                 data_summary=data_summary)


@app.route('/api/click/v1.0/<source_id>/<recommendation_number>')
def redirecturl(source_id, recommendation_number):

    #print(source_id)

    newurl = clicks.find_one({'_id':ObjectId(source_id)}).get('response')[int(recommendation_number)][2]

    clicks.update({'_id': ObjectId(source_id)}, {'$push': {'clicks' : {'response_id': int(recommendation_number), 'time': time.time()}}})

    #print(newurl)
    return redirect(newurl)


class recommendAPI(Resource):
    def __init__(self, recommenders):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url',
                                   type=str,
                                   help='url for document that requires content recommendation')
        # Prepare the list of available engines. This will find all engines
        # that are imported explicitly
        self.engine_classes = Recommender.__subclasses__()
        self.recommenders = recommenders
        super(recommendAPI, self).__init__()

    def get(self, corpus_name):
        # Get the argument: a URL as a string
        start_time = time.time()
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

        response_time = time.time() - start_time
        recdbdoc = recordclicks.getdbdoc( corpus_name, args.url, response_time, recommendation )
        post_id = clicks.insert_one(recdbdoc).inserted_id
        post_id_str = str(post_id)

        recommendation = [( '/api/click/v1.0/' + post_id_str + '/' + str(recommendation.index(item)), item[1], item[2]) for item in recommendation]

        return recommendation


recommenders = dict()
api.add_resource(recommendAPI, '/api/recommend/v1.0/<corpus_name>',
                 resource_class_args=[recommenders])


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
