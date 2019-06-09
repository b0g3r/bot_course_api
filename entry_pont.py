import random

import requests
from flask import Flask, jsonify, request, make_response

import constants

app = Flask(__name__)


@app.route('/api/schedule', methods=['GET'])
def schedule():
    group_number = request.args.get('group')
    if not group_number:
        return make_response(jsonify(error="Invalid group number"), 400)

    schedule_api_response = requests.get(
        constants.SCHEDULE_API.format(group=group_number),
    )
    if schedule_api_response.status_code == 404:
        return make_response(jsonify(error="Unknown group number"), 404)
    else:
        return make_response(jsonify(schedule_api_response.json()), 200)


@app.route('/api/groups', methods=['GET'])
def groups():
    schedule_api_response = requests.get(
        constants.GROUP_API,
    )
    return make_response(jsonify(schedule_api_response.json()), 200)


@app.route('/api/stress', methods=['GET'])
def stress():
    first_letter = request.args.get('first_letter')
    words = constants.STRESSES.copy()
    if first_letter:
        words = [word for word in words if word.lower()[0] == first_letter.lower()]
    word = random.choice(words)
    return make_response(jsonify({'word': word}), 200)


@app.route('/api/millionaire', methods=['GET'])
def millionaire():
    complexity = request.args.get('complexity', 1)
    api_response = requests.get(
        constants.MILLIONAIRE_API,
        params={'q': complexity, 'apikey': constants.MILLIONAIRE_KEY},
    )
    return make_response(jsonify(api_response.json()['data']), api_response.status_code)


if __name__ == '__main__':
    app.run(debug=True)