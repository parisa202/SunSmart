# Useful fuctions for the whole project

from django.shortcuts import redirect
import requests
import json

def api_request(url, parameters=None, request_type='POST'):
    '''
    This fuction is to work with RESTFUL API
    parameters: Dict
    '''

    headers = {'Content-Type': 'application/json'}
            
    if request_type == 'GET':
        response = requests.get(url, json=parameters, headers=headers)
    elif request_type == 'POST':
        response = requests.post(url, json=parameters, headers=headers)
    # Add more request types as needed
    else:
        raise ValueError("Invalid request type")

    return response



def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('CoreApp:login_or_register')  # Redirect to your login URL
        return view_func(request, *args, **kwargs)
    return _wrapped_view