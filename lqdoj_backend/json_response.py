import json


def create_message(message):
    data = {
        'message': message
    }
    return json.dumps(data)