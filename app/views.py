from flask import request, json, abort, jsonify
from app import app
from .utils.numbers import isValidNumber, JSONEncoder
from os import environ
import re
import logging

import json, re
from flask_pymongo import PyMongo

client = PyMongo(app)
db = client.db.numbers

ACCESS_TOKEN = environ.get('ACCESS_TOKEN')

@app.route('/api/blacklist', methods =['POST', 'GET', 'DELETE'])
def Number():
    if request.method == 'POST':
        pre_token = str(request.headers.get('Authorization'))
        token = pre_token.replace('Basic ', '')
        if (token == None) or (token != ACCESS_TOKEN):
            logging.error('Token missing or wrong token')
            return jsonify({'error': 'Unauthorized request'}),401
        td_number = str(request.json.get('talkdesk_number'))
        b_number = str(request.json.get('blacklist_number'))
        if (td_number == None) or (b_number == None) or (isValidNumber(b_number) == False) or (isValidNumber(td_number) == False):
            return jsonify({'error': 'Invalid request'}),400 #invalid request
        else:
            already_present = db.find_one({"blacklist_number": b_number, "talkdesk_number": td_number})
            if already_present == None:
                inserted = db.insert_one({"blacklist_number": b_number, "talkdesk_number": td_number})
                result_id = JSONEncoder().encode(inserted.inserted_id)
                result_id = re.sub('[^0-9a-zA-Z]+', '', result_id)
                return jsonify({'id':result_id}),200 #successfully inserted
            return jsonify({'error': 'Already present.'}),403 #blacklist number already reported


    if request.method == 'GET':
        pre_token = str(request.headers.get('Authorization'))
        token = pre_token.replace('Basic ', '')
        if (token == None) or (token != ACCESS_TOKEN):
            logging.error('Token missing or wrong token')
            return jsonify({'error': 'Unauthorized request'}),401
        td_number = str(request.args.get('talkdesk_number'))
        td_number = re.sub(' ', '+', td_number)
        b_number = str(request.args.get('blacklist_number'))
        b_number = re.sub(' ', '+', b_number)
        if (td_number == None) or (b_number == None) or (isValidNumber(b_number) == False) or (isValidNumber(td_number) == False):
            return jsonify({'error': 'Invalid request'}),400 #invalid request
        else:
            query = {"blacklist_number": b_number, "talkdesk_number": td_number}
            found = db.find_one(query)
            if found != None:
                found_one = json.loads(JSONEncoder().encode(found))
                return json.loads(JSONEncoder().encode(found)),200
            return jsonify({'error': 'Number not found.'}),404

    if request.method == 'DELETE':
        pre_token = str(request.headers.get('Authorization'))
        token = pre_token.replace('Basic ', '')
        if (token == None) or (token != ACCESS_TOKEN):
            logging.error('Token missing or wrong token')
            return jsonify({'error': 'Unauthorized request'}),401
        td_number = str(request.headers.get('talkdesk_number'))
        b_number = str(request.headers.get('blacklist_number'))
        if (td_number == None) or (b_number == None) or (isValidNumber(b_number) == False) or (isValidNumber(td_number) == False):
            return jsonify({'error': 'Invalid request'}),400 #invalid request
        else:
            query = {"blacklist_number": b_number, "talkdesk_number": td_number}
            result = db.delete_one(query)
            if result.deleted_count:
                return jsonify({'deleted':result.deleted_count}),200
            return jsonify({'error': 'Number not found.'}),404



@app.route('/api/blacklist/all', methods = ['GET'])
def api_all():
    pre_token = str(request.headers.get('Authorization'))
    token = pre_token.replace('Basic ', '')
    if (token == None) or (token != ACCESS_TOKEN):
        logging.error('Token missing or wrong token')
        return jsonify({'error': 'Unauthorized request'}),401
    json_dict = {'blacklist_numbers': [], 'total_numbers': 0}
    for doc in db.find():
        temp = json_dict['blacklist_numbers']
        dict = {'_id': str(doc['_id']), 'talkdesk_number': doc['talkdesk_number'], 'blacklist_number': doc['blacklist_number']}
        temp.append(dict)

    json_dict['total_numbers'] = len(json_dict['blacklist_numbers'])
    return json.loads(json.dumps(json_dict)),200
