from flask import jsonify

from . import db

def get_every_game():
    #validate
    response = []
    games = db.readall_db()#pagination in the future

    for game in games:
        #first element is skipped, id
        name, description, genre, developer = game[1:5]
        ram_min, cpu_min, gpu_min, OS_min, storage_min = game[5:10]
        ram_rec, cpu_rec, gpu_rec, OS_rec, storage_rec = game[10:15]
        print(name)
        response.append({
            'info':{
                'name':name,
                'description':description,
                'genre':genre,
                'developer':developer
            },
            'minimum_requirements':{
                'ram_min':ram_min,
                'cpu_min':cpu_min,
                'gpu_min':gpu_min,
                'OS_min':OS_min, 
                'storage_min':storage_min
            },
            'recommended_requirements':{
                'ram_rec':ram_rec, 
                'cpu_rec':cpu_rec,
                'gpu_rec':gpu_rec,
                'OS_rec':OS_rec,
                'storage_rec':storage_rec
            }
        })
    return jsonify(response)
