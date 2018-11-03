# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 11:08:52 2018

@author: Nate
"""

#%%
from flask import Flask, jsonify
import urllib.request, json 
#%%


#%%    
app = Flask(__name__)

with urllib.request.urlopen('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=2') as url:
    trees = json.loads(url.read().decode())

@app.route("/")
@app.route("/home")
def home():
    return "<h1>A Flask App by Nathaniel Cooper</h1>"

@app.route("/trees", methods=['GET'])
def get_trees():
    return jsonify({'trees':trees})

if __name__ == '__main__':
    app.run(debug=True)
#%%