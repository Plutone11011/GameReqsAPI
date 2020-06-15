import json
from flask import jsonify, request, abort

from api.db import db
from api.utils.utils import SUBSECTIONS_GAME, GameEnum
from api.views.validate import validate_filters, validate_pagination


def _process_response(resource_attributes: str, games: tuple, pagination=False):
    """builds a response list of objects for each game"""
    response = []

    def create_response_info(game, section=True):
        nonlocal response_obj
        name, description, developer = game[: GameEnum.DEVELOPER+1]
        response_obj['info'] = {
                SUBSECTIONS_GAME['info'][GameEnum.NAME]: name,
                SUBSECTIONS_GAME['info'][GameEnum.DESCRIPTION]: description,
                SUBSECTIONS_GAME['info'][GameEnum.DEVELOPER]: developer
        }
    
    def create_response_min(game, section=True):
        nonlocal response_obj
        if not section:
            ram_min, cpu_min, gpu_min, OS_min, storage_min = game[GameEnum.RAM_MIN: GameEnum.STORAGE_MIN+1]
        else:
            ram_min, cpu_min, gpu_min, OS_min, storage_min = game[:GameEnum.STORAGE_MIN+1 - GameEnum.RAM_MIN]
        
        response_obj['minimum_requirements'] = {
                SUBSECTIONS_GAME['minimum_requirements'][GameEnum.RAM_MIN - 3]: ram_min,
                SUBSECTIONS_GAME['minimum_requirements'][GameEnum.CPU_MIN - 3]: cpu_min,
                SUBSECTIONS_GAME['minimum_requirements'][GameEnum.GPU_MIN - 3]: gpu_min,
                SUBSECTIONS_GAME['minimum_requirements'][GameEnum.OS_MIN - 3]: OS_min,
                SUBSECTIONS_GAME['minimum_requirements'][GameEnum.STORAGE_MIN - 3]: storage_min
        }
        
    def create_response_rec(game, section=True):
        nonlocal response_obj

        if not section:
            ram_rec, cpu_rec, gpu_rec, OS_rec, storage_rec = game[GameEnum.RAM_REC: GameEnum.STORAGE_REC+1]
        else:
            ram_rec, cpu_rec, gpu_rec, OS_rec, storage_rec = game[: GameEnum.STORAGE_REC+1 - GameEnum.RAM_REC]

        response_obj['recommended_requirements'] = {
            SUBSECTIONS_GAME['recommended_requirements'][GameEnum.RAM_REC - 8]: ram_rec,
            SUBSECTIONS_GAME['recommended_requirements'][GameEnum.CPU_REC - 8]: cpu_rec,
            SUBSECTIONS_GAME['recommended_requirements'][GameEnum.GPU_REC - 8]:gpu_rec,
            SUBSECTIONS_GAME['recommended_requirements'][GameEnum.OS_REC - 8]: OS_rec,
            SUBSECTIONS_GAME['recommended_requirements'][GameEnum.STORAGE_REC - 8]: storage_rec
        }

    for game in games:
        game = list(game)
        id_game = game.pop(0)
        response_obj = {}
        if resource_attributes == 'info':
            create_response_info(game)    
        elif resource_attributes == 'minimum_requirements':
            create_response_min(game)
        elif resource_attributes == 'recommended_requirements':
            create_response_rec(game)
        
        elif not resource_attributes:
            create_response_info(game, False)
            create_response_min(game, False)
            create_response_rec(game, False)

        response.append(response_obj)
        if pagination:
            response[-1]['last_id'] = id_game
    return jsonify(response)


def get_game(resource=None):
    """view for game queries, validate query parameters
        and pass them to db"""
    if resource and resource not in SUBSECTIONS_GAME:
        abort(404)

    limit = None
    last_id = None
    filters = None

    if request.args.get('page'):
        error = validate_pagination(request)

        if error:
            return error
        
        page = json.loads(request.args['page'])
        limit = page['limit']
        last_id = page['last_id']

    if request.args.get('filters'):
        error = validate_filters(request)
        if error:
            return error
        
        filters = json.loads(request.args['filters'])

    if resource:
        games = db.execute_query(*SUBSECTIONS_GAME[resource],
                                 limit=limit,
                                 last_id=last_id,
                                 filter_parameters=filters)
    else:
        games = db.execute_query(limit=limit,
                                 last_id=last_id,
                                 filter_parameters=filters)

    return _process_response(resource, games)