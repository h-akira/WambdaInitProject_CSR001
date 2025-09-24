from wambda.shortcuts import json_response
from datetime import datetime

def auth_status(master):
    """Return authentication status as JSON"""
    is_authenticated = master.request.auth

    response_data = {
        'authenticated': is_authenticated,
        'username': master.request.username if is_authenticated else None,
        'timestamp': datetime.now().isoformat()
    }

    return json_response(master, response_data)

def hello_api(master):
    """Protected Hello World API endpoint"""
    if not master.request.auth:
        return json_response(master, {
            'error': 'Authentication required',
            'message': 'Please login to access this endpoint'
        }, 401)

    response_data = {
        'message': f'Hello, {master.request.username}!',
        'status': 'success',
        'data': {
            'greeting': 'Hello World from WAMBDA CSR001 API',
            'user': master.request.username,
            'timestamp': datetime.now().isoformat()
        }
    }

    return json_response(master, response_data)