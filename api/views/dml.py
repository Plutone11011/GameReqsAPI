import json
from flask import current_app, request, Response
from marshmallow import ValidationError

from api.db import db
from api.db.model import GameSchema, Game, UpdateGameSchema
from api.views.validate import validate
from api.utils.authorizers import require_api_key


@require_api_key
def insert_game():
    game_schema = GameSchema()
    try:
        game = game_schema.load(request.json)
        id = db.insert_game(game)
        return Response(json.dumps({'insertedGameId': id}), status=201, mimetype='application/json')
    except json.JSONDecodeError as err:
        return validate({'insert_body': err.msg})
    except ValidationError as err:
        return validate(err.messages)


@require_api_key
def update_game():
    game_schema = UpdateGameSchema()
    try:
        game = game_schema.load(request.json)
        rowcount = db.update_game(game)
        if rowcount:
            return '', 200
        else:
            return json.dumps('No resources to update'), 404
    except json.JSONDecodeError as err:
        return validate({'update_body': err.msg})
    except ValidationError as err:
        return validate(err.messages)


@require_api_key
def delete_game(id_game=None):
    rowcount = db.delete_game(id_game)

    if rowcount:
        return '', 204
    else:
        return json.dumps('No resources to delete'), 404
