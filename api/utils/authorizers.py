import os
import json
from functools import wraps

from flask import request


def require_api_key(view_func):
    @wraps(view_func)
    def authorize(*args, **kwargs):
        key = os.getenv('API_KEY')
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == key:
            return view_func(*args, **kwargs)
        else:
            return json.dumps('Forbidden'), 401
    return authorize
