from json import dumps
from flask import current_app, request, Response

from . import db

def validate(json_data):
    if not json_data['name']:
        print('Error for null name')
    
    if not json_data['ram_min']:
        print('Error for null ram_min')
    
    if not json_data['cpu_min']:
        print('Error for null cpu_min')
    
    if not json_data['gpu_min']:
        print('Error for null gpu_min')
    
    if not json_data['storage_min']:
        print('Error for null storage_min')

    if not json_data['OS_min']:
        print('Error for null OS_min')
    

def insert_game():
    validate(request.json)

    game = (request.json['name'], request.json['description'], request.json['genre'], 
    request.json['developer'], request.json['ram_min'],
     request.json['cpu_min'], request.json['gpu_min'], 
     request.json['OS_min'], request.json['storage_min'], 
     request.json['ram_rec'], request.json['cpu_rec'], request.json['gpu_rec']
     ,request.json['OS_rec'], request.json['storage_rec'])
    

    id = db.insert_db(game)
    return Response(dumps({'insertedGameId': id}), status=201, mimetype='application/json')

def delete_game():

    rowcount = db.deleteall_db()

    return '',204    