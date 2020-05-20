from flask import current_app, request

import db

@current_app.route('/api/v1/games/', method=['POST'])
def insert_game():
    if not request.form['name'] or not request.form['description']:
        #name and description are a must
        #application json error
        print('Error here')
    game = (request.form['name'], request.form['description'], request.form['genre'], request.form['description'], request.form['developer'], request.form['ram_min'],
     request.form['cpu_min'], request.form['gpu_min'], request.form['OS_min'], request.form['storage_min'], request.form['ram_rec'], request.form['cpu_rec'], request.form['gpu_rec']
     ,request.form['OS_rec'], request.form['storage_rec'])
    
    id = db.insert_db(game)
    return {
        "insertedGameId": id
    }
    