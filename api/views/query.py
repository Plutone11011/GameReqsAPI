from flask import jsonify

from api.db import db


def get_every_game():

    response = []
    games = db.readall_db()  #pagination in the future

    for game in games:

        name, description, developer = game[1:4]   #first element is skipped, id
        ram_min, cpu_min, gpu_min, OS_min, storage_min = game[4:9]
        ram_rec, cpu_rec, gpu_rec, OS_rec, storage_rec = game[9:14]
        print(name)
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
