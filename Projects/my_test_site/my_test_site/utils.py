from functools import wraps
from django.http import HttpResponse
import json

def allow_cors(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Origin, Content-Type, Accept"
        return response
    return wrapper


def get_post_data(request):
    data = json.loads(request.body.decode('utf-8'))
    return data