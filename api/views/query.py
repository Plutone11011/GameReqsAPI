import json
from flask import jsonify, request, Response

from api.db import db
from api.utils.GameEnum import GameEnum
from api.utils.utils import SQL_OPERATOR_URI_MAPPER


def _process_response(response: list, games: tuple, pagination=False):
    for game in games:
        #print(game)
        game = list(game)
        id_game = game.pop(0)

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
    elif not isinstance(page_parameters.get('limit'), int):
        problem['invalid-params'].append({
            'name': 'limit',
            'reason': 'Maximum number of results has to be a number'
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
    elif not isinstance(page_parameters.get('limit'), int):
        problem['invalid-params'].append({
            'name': 'last_id',
            'reason': 'Last inserted id has to be a number'
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


def validate_filters(request):
    problem = {
        'type': 'https://tools.ietf.org/html/rfc7807#section-3',
        'title': 'Your request parameters weren\'t valid.',
        'invalid-params': []
    }

    try:
        filter_parameters = json.loads(request.args['filters'])
    except json.decoder.JSONDecodeError as json_error:
        problem['invalid-params'].append({
            'name': 'filters',
            'reason': json_error.msg
        })
        return Response(json.dumps(problem), status=400, mimetype='application/problem+json')

    for filter_param in filter_parameters:
        if not filter_param.get('op'):
            problem['invalid-params'].append({
                'name': 'op',
                'reason': 'Operation parameter must be provided with filters'
            })
        elif filter_param.get('op') not in SQL_OPERATOR_URI_MAPPER:
            problem['invalid-params'].append({
                'name': 'op',
                'reason': 'Operation parameter does not have a valid value'
            })
        if not filter_param.get('memory'):
            problem['invalid-params'].append({
                'name': 'memory',
                'reason': 'memory parameter must be provided with filters'
            })
        elif filter_param.get('memory') not in ['ram_min', 'ram_rec', 'storage_min', 'storage_rec']:
            problem['invalid-params'].append({
                'name': 'memory',
                'reason': 'Memory parameter does not have a valid value'
            })
        if not filter_param.get('value'):
            problem['invalid-params'].append({
                'name': 'value',
                'reason': 'Value parameter must be provided with filters'
            })
        elif not isinstance(filter_param.get('value'), int):
            problem['invalid-params'].append({
                'name': 'value',
                'reason': 'Value parameter does not have a valid value'
            })
        if len(problem['invalid-params']):
            return Response(json.dumps(problem), status=400, mimetype='application/problem+json')
        else:
            return None


def get_game():
    if request.args.get('page'):
        error = validate_pagination(request)

        if error:
            return error

        return get_paginated_games(json.loads(request.args['page']))

    if request.args.get('filters'):
        print(request.args.get('filters'))
        error = validate_filters(request)
        if error:
            return error
        return get_filtered_memory_games(json.loads(request.args.get('filters')))

    response = []
    games = db.readall()

    return _process_response(response, games)


def get_paginated_games(page_parameters: dict):
    response = []

    # last id is the id returned by this endpoint, the starting id for the next page
    games = db.read_paginated(page_parameters['limit'], page_parameters['last_id'])

    return _process_response(response, games, True)


def get_filtered_memory_games(filter_parameters):
    response = []

    games = db.read_filtered_by_memory(filter_parameters)

    return _process_response(response, games)
