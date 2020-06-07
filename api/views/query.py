from flask import jsonify, request

from api.db import db

#defines ranges for each section in the response tuple
def response_slice(section):

    section_indexes = {
        'info': slice(1,4),
        'minimum_requirements': slice(4,9), 
        'recommended_requirements':slice(9,14)
    }

    return section_indexes[section]

def _process_get_response(response, games):
    for game in games:

        name, description, developer = game[response_slice('info')]   #first element is skipped, id
        ram_min, cpu_min, gpu_min, OS_min, storage_min = game[response_slice('minimum_requirements')]
        ram_rec, cpu_rec, gpu_rec, OS_rec, storage_rec = game[response_slice('recommended_requirements')]
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
    return jsonify(response)

def get_every_game():

    response = []
    games = db.readall_db()

    return _process_get_response(response, games)



def get_paginated_games():
    response = []

    #last id is the id returned by this endpoint, the starting id for the next page
    print(request.args)
    games = db.read_paginated_db(request.args['limit'],request.args['last_id'])

    return _process_get_response(response, games)