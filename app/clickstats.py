import json
from bson import json_util
import pymongo
from pymongo import MongoClient

client = MongoClient('db')
db = client.clickdb
clicks = db.clicks


def getdatasummary():
    '''This function returns some summary data from the click database. This will
    be used in the dashboard view.
    '''
    # First we will do some counting
    # Get the total number of API requests = number of click documents
    counter = clicks.count()
    # Get the average response time of all time
    cursor = clicks.find()
    average_clickcountperrequest = 0.0
    clickcount = 0
    average_response_time = 0.0
    average_click_delay = 0.0
    average_first_score = 0.0
    average_score = 0.0
    countsuccess = 0
    for document in cursor:
        if len(document['response']) != 5:
            continue
        countsuccess += 1
        time_of_request = document['time']
        average_response_time += document['response_time']
        # loop over all clicks inside the response document
        for click in document['clicks']:
            clickcount += 1
            average_click_delay += click['time'] - time_of_request
        average_first_score += float(document['response'][0][1])
        for response in document['response']:
            average_score += float(response[1])

    average_click_delay = average_click_delay/clickcount
    average_response_time = average_response_time/countsuccess
    average_clickcountperrequest = clickcount/countsuccess
    average_first_score = average_first_score/countsuccess
    average_score = average_score/(countsuccess * 5)

    return {'countsuccess': countsuccess,
            'counter': counter,
            'average_response_time': average_response_time,
            'average_click_delay': average_click_delay,
            'clickcount': clickcount,
            'average_clickcountperrequest': average_clickcountperrequest,
            'average_first_score': average_first_score,
            'average_score': average_score,
            }


def getalldata():
    ''' This function passes on all available data in the database. This can
    then be used in the graphing code.
    '''
    cursor = clicks.find()
    json_data = []
    # We only want to use successful requests for now, so
    # ignore all the documents that do not have a valid response.
    for document in cursor:
        if len(document['response']) != 5:
            continue
        json_data.append(document)
    json_data = json.dumps(json_data, default=json_util.default)
    return json_data
