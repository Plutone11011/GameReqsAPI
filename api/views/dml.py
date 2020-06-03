from json import dumps
from flask import current_app, request, Response

from api.db import db


def validate(request):

    #response in application/problem+json format
    problem = {
        'type': 'https://tools.ietf.org/html/rfc7807#section-3',
        'title': 'Your request parameters didn\'t validate.',
        'invalid-params': []
    }
    if not request['name']:
        problem['invalid-params'].append({
            'name': 'name',
            'reason': 'Game name must be provided'
        })
    
    # if not request['ram_min']:
    #     problem['invalid-params'].append({
    #         'name': 'ram_min',
    #         'reason': 'Minimum requirements (ram) must be provided'
    #     })
    #
    # if not request['cpu_min']:
    #     problem['invalid-params'].append({
    #         'name': 'cpu_min',
    #         'reason': 'Minimum requirements (cpu) must be provided'
    #     })
    # if not request['gpu_min']:
    #     problem['invalid-params'].append({
    #         'name': 'gpu_min',
    #         'reason': 'Minimum requirements (gpu) must be provided'
    #     })
    # if not request['storage_min']:
    #     problem['invalid-params'].append({
    #         'name': 'storage_min',
    #         'reason': 'Minimum requirements (storage) must be provided'
    #     })
    # if not request['OS_min']:
    #     problem['invalid-params'].append({
    #         'name': 'OS_min',
    #         'reason': 'Minimum requirements (OS) must be provided'
    #     })

    if len(problem['invalid-params']):
        print('There are errors')
        return Response(dumps(problem), status=400, mimetype='application/problem+json')
    else:
        return None    


def insert_game():
    has_error = validate(request.json)
    if has_error:
        return has_error

    game = (request.json['name'], request.json['description'],
            request.json['developer'], request.json['ram_min'],
            request.json['cpu_min'], request.json['gpu_min'],
            request.json['OS_min'], request.json['storage_min'],
            request.json['ram_rec'], request.json['cpu_rec'], request.json['gpu_rec'],
            request.json['OS_rec'], request.json['storage_rec'])
    
    id = db.insert_db(game)
    return Response(dumps({'insertedGameId': id}), status=201, mimetype='application/json')


def delete_game():

    rowcount = db.deleteall_db()

    return '', 204
