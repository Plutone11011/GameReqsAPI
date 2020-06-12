from json import dumps
from flask import current_app, request, Response

from api.db import db


def validate(req):

    #response in application/problem+json format
    problem = {
        'type': 'https://tools.ietf.org/html/rfc7807#section-3',
        'title': 'Your request parameters weren\'t valid.',
        'invalid-params': []
    }
    if not req.get('name'):
        problem['invalid-params'].append({
            'name': 'name',
            'reason': 'Game name must be provided'
        })

    if len(problem['invalid-params']):
        return Response(dumps(problem), status=400, mimetype='application/problem+json')
    else:
        return None    


def insert_game():
    error = validate(request.json)
    if error:
        return error

    game = (request.json['name'], request.json['description'],
            request.json['developer'], request.json['ram_min'],
            request.json['cpu_min'], request.json['gpu_min'],
            request.json['OS_min'], request.json['storage_min'],
            request.json['ram_rec'], request.json['cpu_rec'], request.json['gpu_rec'],
            request.json['OS_rec'], request.json['storage_rec'])
    
    id = db.insert(game)
    return Response(dumps({'insertedGameId': id}), status=201, mimetype='application/json')


def delete_game():

    rowcount = db.deleteall()

    return '', 204
