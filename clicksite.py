#!/usr/bin/env python

import os
from flask import Flask, json, jsonify, render_template, redirect, request

import random

app = Flask(__name__)


dbsite = os.path.realpath(os.path.dirname(__file__))

#Loads the file with the sites data.
json_file = open(os.path.join(dbsite, 'SiteList.json'))
data = json.load(json_file)
json_file.close()

inputid = None

#Gets the input url from user.

@app.route('/')
def enterurl():
    return render_template('enterurl.html')

#Get the url and display the list of suggested sites.

@app.route('/', methods = ['POST'])
def show_rec():
    inputurl = request.form['inputurl']

    #here is the missing part where it talks to page suggestion, and returns suggestions

    #see if the input url is already in site list
    #Not the best now. Will think of way to fix.
    for items in data.items():
        if inputurl in items[1].get('url'):
            inputid = items[0]
            break
        else:
            inputid = 'idx'

    return render_template('sitelist.html', data = data, inputid = inputid)



@app.route('/<post_id>')
def show_post(post_id):

    #This is currently not the most ideal system to get the to and from info
    if 'n' in post_id:
        post_from = post_id.split('n')[0]
        post_to = post_id.split('n')[1]
    else:
        return 'id does not exist'

    #Record the to and from info in the sitelist file
    if post_to and post_from in data:

        if data[post_to].get(post_from) :
            data[post_to][post_from] +=1
        else:
            data[post_to][post_from] = 1

        json_file = open(os.path.join(dbsite, 'SiteList.json'), "w+")
        json_file.write(json.dumps(data))
        json_file.close()

        return redirect(data[post_to]['url'])

    elif post_to in data:
        return redirect(data[post_to]['url'])

    else:
        return 'id does not exist'


if __name__ == "__main__":
    app.run()
