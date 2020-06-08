from flask import jsonify, request

from api.db import db
from api.utils.GameEnum import GameEnum


def _process_get_response(response, games):
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
    return response, id_game


def get_every_game():

    response = []
    games = db.readall_db()

    return jsonify(_process_get_response(response, games)[0])


def get_paginated_games():
    response = []

    # last id is the id returned by this endpoint, the starting id for the next page
    print(request.args)
    games = db.read_paginated_db(request.args['limit'], request.args['last_id'])

    response, id_game = _process_get_response(response, games)
    response[-1].setdefault('last_id', id_game)
    return jsonify(response)
