import json
from flask import jsonify, request, abort
from marshmallow import ValidationError

from api.db import db
from api.utils.utils import SUBSECTIONS_GAME
from api.views.validate import validate
from api.db.model import PageSchema, FilterSchema


def _process_response(resource_attributes: str, games: tuple, pagination=False):
    """builds a response list of objects for each game"""
    response = []

    for game in games:
        response_obj = {}
        response_obj['id'] = game.get('id')
        # add different subsections in case it's been specified
        # otherwise add everything
        if resource_attributes == 'info' or not resource_attributes:
            response_obj['info'] = {
                'name': game.get('name'),
                'description': game.get('description'),
                'developer': game.get('developer')
            }
        if resource_attributes == 'minimum_requirements' or not resource_attributes:
            response_obj['minimum_requirements'] = {
                 'ram_min': game.get('ram_min'),
                 'cpu_min': game.get('cpu_min'),
                 'storage_min': game.get('storage_min'),
                 'gpu_min': game.get('gpu_min'),
                 'OS_min': game.get('OS_min')
            }
        if resource_attributes == 'recommended_requirements' or not resource_attributes:
            response_obj['recommended_requirements'] = {
                'ram_rec': game.get('ram_rec'),
                'cpu_rec': game.get('cpu_rec'),
                'storage_rec': game.get('storage_rec'),
                'gpu_rec': game.get('gpu_rec'),
                'OS_rec': game.get('OS_rec')
            }

        response.append(response_obj)
    return jsonify(response)


def get_game(resource=None):
    """view for game queries, validate query parameters
        and pass them to db"""
    if resource and resource not in SUBSECTIONS_GAME:
        return json.dumps(f'No endpoint for resource {resource}'), 404

    limit = None
    last_id = None
    filters = None
    name = request.args.get('name')

    if request.args.get('page'):
        page_schema = PageSchema()
        try:
            page = page_schema.loads(request.args['page'])
            limit = page.limit
            last_id = page.last_id
        except json.JSONDecodeError as err:
            return validate({'page': err.msg})
        except ValidationError as err:
            return validate(err.messages)

    if request.args.get('filters'):
        filter_schema = FilterSchema(many=True)
        
        try:
            filters = filter_schema.loads(request.args['filters'])
        except json.JSONDecodeError as err:
            return validate({'filters': err.msg})
        except ValidationError as err:
            return validate(err.messages)

    if resource:
        games = db.game_query(*SUBSECTIONS_GAME[resource],
                              limit=limit,
                              last_id=last_id,
                              filter_parameters=filters,
                              name=name)
    else:
        games = db.game_query(limit=limit,
                              last_id=last_id,
                              filter_parameters=filters,
                              name=name)
    if games:
        return _process_response(resource, games)
    else:
        return json.dumps('No resources to get'), 404