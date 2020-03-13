import re
from app import app
import json
from bson import ObjectId



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def isValidNumber(phone_number):
    print(type(phone_number))
    print(phone_number)
    e164_pattern = re.compile('^\+[1-9]\d{1,14}$')
    m = e164_pattern.match(phone_number)
    print(m)
    if m:
        return True
    else:
        return False
