import json
from flask import jsonify, request, Response

from api.db import db
from api.utils.GameEnum import GameEnum


def _process_response(response: list, games: tuple, pagination: bool):
    for game in games:
        id_game = list(game).pop(0)

        name, description, developer = game[GameEnum.response_slice('info')]
        ram_min, cpu_min, gpu_min, OS_min, storage_min = game[GameEnum.response_slice('minimum_requirements')]
        ram_rec, cpu_rec, gpu_rec, OS_rec, storage_rec = game[GameEnum.response_slice('recommended_requirements')]
        response.append({
            'info': {
                'name': name,
                'description': description,
                'developer': developer
            },
            'minimum_requirements': {
                'ram_min': ram_min,
                'cpu_min': cpu_min,
                'gpu_min': gpu_min,
                'OS_min': OS_min,
                'storage_min': storage_min
            },
            'recommended_requirements': {
                'ram_rec': ram_rec,
                'cpu_rec': cpu_rec,
                'gpu_rec':gpu_rec,
                'OS_rec': OS_rec,
                'storage_rec': storage_rec
            }
        })
        if pagination:
            response[-1]['last_id'] = id_game
    return jsonify(response)


def validate_pagination(request):
    problem = {
        'type': 'https://tools.ietf.org/html/rfc7807#section-3',
        'title': 'Your request parameters weren\'t valid.',
        'invalid-params': []
    }

    try:
        page_parameters = json.loads(request.args['page'])
    except json.decoder.JSONDecodeError as json_error:
        problem['invalid-params'].append({
            'name': 'page',
            'reason': json_error.msg
        })
        return Response(json.dumps(problem), status=400, mimetype='application/problem+json')

    if not page_parameters.get('limit') and page_parameters.get('limit') != 0:
        problem['invalid-params'].append({
            'name': 'limit',
            'reason': 'Maximum number of results must be provided with pagination'
        })
    elif page_parameters.get('limit') < 0:
        problem['invalid-params'].append({
            'name': 'limit',
            'reason': 'Maximum number of results can\'t be negative'
        })

    if not page_parameters.get('last_id') and page_parameters.get('last_id') != 0:
        problem['invalid-params'].append({
            'name': 'last_id',
            'reason': 'Last inserted id must be provided with pagination'
        })
    elif page_parameters.get('last_id') < 0:
        problem['invalid-params'].append({
            'name': 'last_id',
            'reason': 'Last inserted id can\'t be negative'
        })
    if len(problem['invalid-params']):
        return Response(json.dumps(problem), status=400, mimetype='application/problem+json')
    else:
        return None


def get_every_game():
    if request.args.get('page'):
        page_parameters = {}
        error = validate_pagination(request)

        if error:
            return error

        return get_paginated_games(json.loads(request.args['page']))
    response = []
    games = db.readall_db()

    return _process_response(response, games, False)


def get_paginated_games(page_parameters: dict):
    response = []

    # last id is the id returned by this endpoint, the starting id for the next page
    games = db.read_paginated_db(page_parameters['limit'], page_parameters['last_id'])

    return _process_response(response, games, True)
