import json
from flask import current_app, request, Response
from marshmallow import ValidationError

from api.db import db
from api.db.model import GameSchema, Game
from . import validate


def insert_game():
    game_schema = GameSchema()
    try:
        game = game_schema.load(request.json)
        id = db.insert(game)
        return Response(json.dumps({'insertedGameId': id}), status=201, mimetype='application/json')
    except json.JSONDecodeError as err:
        return validate.validate({'insert_body': err.msg})
    except ValidationError as err:
        return validate.validate(err.messages)


def delete_game():

    rowcount = db.deleteall()

    return '', 204
