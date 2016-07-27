#!/usr/bin/env python
import time

def getdbdoc(corpus_name, inputurl, response_time, recommendation):
    dbdoc = {
        "version": 1.0,
        "corpus": corpus_name,
        "request" : inputurl,
        "time": time.time(),
        "response_time": response_time,
        "response": recommendation,
         "engine" : "speech",
         "experiment_id": 1,
         "clicks": []
     }

    return dbdoc   
