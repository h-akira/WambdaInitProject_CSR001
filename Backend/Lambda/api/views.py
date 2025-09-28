from wambda.shortcuts import json_response
from datetime import datetime

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