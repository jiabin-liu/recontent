import json
import pymongo
from pymongo import MongoClient

client = MongoClient('db')
db = client.clickdb
clicks = db.clicks


def getdatasummary():
    """
    This function returns some summary data from the click database.
    """
    # First we will do some counting
    # Get the total number of API requests = number of click documents
    counter = clicks.count()
    # Get the average response time of all time
    cursor = clicks.find()
    clickcount = 0
    average_response_time = 0.0
    average_click_delay = 0.0
    for document in cursor:
        time_of_request = document['time']
        average_response_time += document['response_time']
        # loop over all clicks inside the response document
        for click in document['clicks']:
            clickcount += 1
            average_click_delay += click['time'] - time_of_request
    average_click_delay = average_click_delay/clickcount
    average_response_time = average_response_time/counter

    # Calculate the overall average response time
    return {'counter': counter,
            'average_response_time': average_response_time,
            'average_click_delay': average_click_delay,
            'clickcount': clickcount}
