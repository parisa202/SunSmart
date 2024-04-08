# Useful fuctions for the whole project

import requests
import json

def api_request(url, parameters=None, request_type='POST'):
    '''
    This fuction is to work with RESTFUL API
    parameters: Dict
    '''
    json_data = json.dumps(parameters)
    headers = {'Content-Type': 'application/json'}
            
    if request_type == 'GET':
        response = requests.get(url, json=json_data, headers=headers)
    elif request_type == 'POST':
        response = requests.post(url, params=json_data, headers=headers)
    # Add more request types as needed
    else:
        raise ValueError("Invalid request type")

    return response