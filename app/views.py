from flask import request, json, abort, jsonify
from app import app
from .utils.numbers import isValidNumber, JSONEncoder
#from models import Number

import json, re
from flask_pymongo import PyMongo

client = PyMongo(app)
db = client.db.numbers


ACCESS_TOKEN = 'test'


@app.route('/api/v1/numbers', methods =['POST', 'GET', 'DELETE'])
def Number():
    if request.method == 'POST':
        token = request.headers.get('token')
        td_number = str(request.json.get('talkdesk_number'))
        b_number = str(request.json.get('blacklist_number'))
        print(token)
        print(td_number)
        print(b_number)
        if (token == None) or (td_number == None) or (b_number == None) or (isValidNumber(b_number) == False) or (isValidNumber(td_number) == False):
            return jsonify({'error': 'Invalid request'}),400 #invalid request
        elif token != ACCESS_TOKEN:
            return jsonify({'error': 'Unauthorized request'}),401 #unauthorized
        else:
            already_present = db.find_one({"blacklist_number": b_number, "talkdesk_number": td_number})
            if already_present == None:
                inserted = db.insert_one({"blacklist_number": b_number, "talkdesk_number": td_number})
                result_id = JSONEncoder().encode(inserted.inserted_id)
                result_id = re.sub('[^0-9a-zA-Z]+', '', result_id)
                print(result_id)
                return jsonify({'id':result_id}),200 #successfully inserted
            return jsonify({'error': 'Already present.'}),400 #blacklist number already reported


    if request.method == 'GET':
        token = request.headers.get('token')
        td_number = request.headers.get('talkdesk_number')
        print(td_number)
        b_number = request.headers.get('blacklist_number')
        print(b_number)
        if (token == None) or (td_number == None) or (b_number == None) or (isValidNumber(b_number) == False) or (isValidNumber(td_number) == False):
            return jsonify({'error': 'Invalid request'}),400 #invalid request
        elif token != ACCESS_TOKEN:
            return jsonify({'error': 'Unauthorized request'}),401 #unauthorized
        else:
            query = {"blacklist_number": b_number, "talkdesk_number": td_number}
            found = db.find_one(query)
            if found != None:
                found_one = json.loads(JSONEncoder().encode(found))
                print(found_one)
                return json.loads(JSONEncoder().encode(found)),200
            return jsonify({'error': 'Number not found.'}),404

    if request.method == 'DELETE':
        token = request.headers.get('token')
        td_number = str(request.headers.get('talkdesk_number'))
        b_number = str(request.headers.get('blacklist_number'))
        if (token == None) or (td_number == None) or (b_number == None) or (isValidNumber(b_number) == False) or (isValidNumber(td_number) == False):
            return jsonify({'error': 'Invalid request'}),400 #invalid request
        elif token != ACCESS_TOKEN:
            return jsonify({'error': 'Unauthorized request'}),401 #unauthorized
        else:
            query = {"blacklist_number": b_number, "talkdesk_number": td_number}
            result = db.delete_one(query)
            if result.deleted_count:
                return jsonify({'deleted':result.deleted_count}),200
            return jsonify({'error': 'Number not found.'}),404



@app.route('/api/v1/numbers/all', methods = ['GET'])
def api_all():
    token = request.headers.get('token')
    if token is None:
        return jsonify({'error': 'Invalid request'}),400
    elif token != ACCESS_TOKEN:
        return jsonify({'error': 'Unauthorized request'}),401
    else:
        json_dict = {'blacklist_numbers': [], 'total_numbers': 0}
        for doc in db.find():
            temp = json_dict['blacklist_numbers']
            dict = {'_id': str(doc['_id']), 'talkdesk_number': doc['talkdesk_number'], 'blacklist_number': doc['blacklist_number']}
            temp.append(dict)

        json_dict['total_numbers'] = len(json_dict['blacklist_numbers'])
        return json.loads(json.dumps(json_dict)),200
