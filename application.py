import random

import json
import os
from flask import Flask, Response

application = app = Flask(__name__)


@app.route('/faq')
def get_faq():
    folder = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(folder, 'faq.json')

    with open(data_path) as file:
        response_data = json.loads(file.read())

    return Response(response=json.dumps(response_data), content_type='application/json')

@app.route('/')
def accept_question():

    data_path = ""
    #file_index = random.randint(0, 5)
    file_index = 4
    folder = os.path.dirname(os.path.abspath(__file__))
    if file_index == 0:
        data_path = os.path.join(folder, 'mock_response.json')
    elif file_index == 1:
        data_path = os.path.join(folder, 'mock_response.json')
    elif file_index == 2:
        data_path = os.path.join(folder, 'linechart.json')
    elif file_index == 3:
        data_path = os.path.join(folder, 'bubblechart.json')
    elif file_index == 4:
        data_path = os.path.join(folder, 'mutiplelinechart.json')
    elif file_index == 5:
        data_path = os.path.join(folder, 'scatterchart.json')


    with open(data_path) as file:
        suggested_charts = json.loads(file.read())

    index = random.randint(0, len(suggested_charts)-1)
    print(json.dumps(suggested_charts[index]))
    return Response(response=json.dumps(suggested_charts[index]), content_type='application/json')


if __name__ == '__main__':
    application.run(host='0.0.0.0', port='5500')
