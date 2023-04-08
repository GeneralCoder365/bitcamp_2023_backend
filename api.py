from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
from werkzeug.wrappers import Response

import requests
import json
from requests.models import Response
from datetime import datetime, date, time, timedelta

import sys, logging
import multiprocessing
import time






app = Flask(__name__)
api = Api(app)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# @app.route('/getBaseURL', methods=['GET'])
# def getBaseURL():
#     query = (request.args.get('query')).lower()
    
#     return get_base_url(query)

# @app.route('/getInitialData', methods=['POST'])
# def getInitialData():
#     request_data = request.get_json()
#     # print(request_data)
#     base_url = request_data["base_url"]
#     base_target = request_data["base_target"]
#     headers = request_data["headers"]
    
#     return get_canvas_course_data(base_url, base_target, headers)



app.debug = True

if __name__ == '__main__':
    app.run()