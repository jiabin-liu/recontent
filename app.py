#!/usr/bin/env python
from flask import Flask, jsonify, make_response
app = Flask(__name__)

test = [
    {
        'id': 1,
        'title': 'test1',
        'url': 'http://www.google.com'
    },
    {
        'id': 2,
        'title': 'test2',
        'url': 'http://www.google.com'
    }
]


@app.route('/')
def index():
    return "Content recommendation rocks!"


@app.route('/api/recommend/test', methods=['GET'])
def get_test():
    return jsonify({'test': test})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
