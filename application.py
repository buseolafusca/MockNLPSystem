import json
import os
import random
import flask
import numpy as np

application = app = flask.Flask(__name__)
mock_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model_questions.json')
number_of_faqs = 8
always_question = "How many people visited A&E in June and July by gender and race?"


def get_n_questions(file_name, n):
    with open(file_name) as file:
        json_data = json.loads(file.read())
    questions = np.array([q['responseData']['summary']['question'] for q in json_data])
    if len(questions) < n:
        n = len(questions)
    n_questions = list(questions[random.sample(range(0, len(questions)-1), n)])
    if always_question not in n_questions:
        n_questions[0] = always_question
        print('Not in FAQ')
    return n_questions


@app.route('/faq')
def get_faq():
    folder = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(folder, 'response_template.json')

    with open(data_path) as file:
        response_data = json.loads(file.read())

    questions = get_n_questions(mock_data, number_of_faqs)
    response_data['responseData']['questions'] = questions
    return flask.Response(response=json.dumps(response_data), content_type='application/json')


@app.route('/')
@app.route('/random_question', methods=['GET', 'POST'])
def random_question():
    data_path = ""
    # file_index = random.randint(0, 5)
    file_index = 6
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
    elif file_index == 6:
        data_path = os.path.join(folder, 'smallerfixedrow2.json')

    with open(data_path) as file:
        suggested_charts = json.loads(file.read())

    index = random.randint(0, len(suggested_charts)-1)
    print(json.dumps(suggested_charts[index]))
    return flask.Response(response=json.dumps(suggested_charts[index]), content_type='application/json')


@app.route('/question', methods=['GET', 'POST'])
def accept_question():
    question = flask.request.data.decode('utf-8')

    with open(mock_data) as file:
        json_data = json.loads(file.read())

    print(question)

    questions = [q for q in json_data if q['responseData']['summary']['question'] == question]
    print(len(questions))
    if not questions:
        return flask.redirect(flask.url_for('random_question'), code=307)
    else:
        chart_data = questions[0]
    print(json.dumps(chart_data))
    return flask.Response(response=json.dumps(chart_data), content_type='application/json')


if __name__ == '__main__':
    application.run(host='0.0.0.0', port='5500')
