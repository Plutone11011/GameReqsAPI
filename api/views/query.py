import json
from flask import jsonify, request

from api.db import db
from api.utils.GameEnum import GameEnum
from api.views.validate import validate_filters, validate_pagination


def _process_response(response: list, games: tuple, pagination=False):
    for game in games:
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


def get_game():
    response = []
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
