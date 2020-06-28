import json
from api.run import myapp as app
from dotenv import load_dotenv


class TestController(object):

    @classmethod
    def setup_class(cls):
        load_dotenv('.flaskenv')
        cls.client = app.test_client()
        cls.headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'cf7c9541c2b477a00cbe2549cda1b5c118c75f7f7a2448eebd831611'
        }
        cls.wrong_headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'hogehoge'
        }
        cls.create_data = json.dumps({
            'name': 'name_01',
            'description': 'description_01',
            'developer': 'developer_01',
            'ram_min': 1,
            'cpu_min': 'cpu_min_01',
            'gpu_min': 'gpu_min_01',
            'OS_min': 'OS_min_01',
            'storage_min': 1,
            'ram_rec': 1,
            'cpu_rec': 'cpu_rec_01',
            'gpu_rec': 'gpu_rec_01',
            'OS_rec': 'OS_rec_01',
            'storage_rec': 1,
        })
        cls.update_data = {
            'name': 'name_02',
            'description': 'description_02',
            'developer': 'developer_02',
            'ram_min': 2,
            'cpu_min': 'cpu_min_02',
            'gpu_min': 'gpu_min_02',
            'OS_min': 'OS_min_02',
            'storage_min': 2,
            'ram_rec': 2,
            'cpu_rec': 'cpu_rec_02',
            'gpu_rec': 'gpu_rec_02',
            'OS_rec': 'OS_rec_02',
            'storage_rec': 2,
        }

    def test_insert_game(self):
        path = '/api/v1/games'
        response = self.client.post(path, headers=self.headers, data=self.create_data)
        print(response.get_data())
        assert response.status_code == 201

    def test_insert_game_unauthorized(self):
        path = '/api/v1/games'
        response = self.client.post(path, headers=self.wrong_headers, data=self.create_data)
        print(response.get_data())
        assert response.status_code == 401

    def test_get_game(self):
        path = '/api/v1/games?name=vrkshop'
        response = self.client.get(path, headers=self.headers)
        print(response.get_data())
        assert response.status_code == 200

    def test_get_game_unauthorized(self):
        path = '/api/v1/games?name=vrkshop'
        response = self.client.get(path, headers=self.wrong_headers)
        print(response.get_data())
        assert response.status_code == 401

    # if execute this, all data will be deleted. so this test is comment out
    # def test_delete_game(self):
    #    path = '/api/v1/games'
    #    response = self.client.post(path, headers=self.headers, data=self.create_data)
    #    data = json.loads(response.get_data())
    #    game_id = data.get('insertedGameId')
    #    path = path + f'/{game_id}'
    #    response = self.client.delete(path, headers=self.headers)
    #    print(response.get_data)
    #    assert response.status_code == 204

    def test_delete_game_unauthorized(self):
        path = '/api/v1/games/1'
        response = self.client.delete(path, headers=self.wrong_headers)
        print(response.get_data)
        assert response.status_code == 401

    def test_delete_game_by_id(self):
        path = '/api/v1/games'
        response = self.client.post(path, headers=self.headers, data=self.create_data)
        data = json.loads(response.get_data())
        game_id = data.get('insertedGameId')
        path = path + f'/{game_id}'
        response = self.client.delete(path, headers=self.headers)
        print(response.get_data)
        assert response.status_code == 204

    def test_delete_game_by_id_unzuthorized(self):
        path = '/api/v1/games/1'
        response = self.client.delete(path, headers=self.wrong_headers)
        print(response.get_data)
        assert response.status_code == 401

    def test_get_game_by_resource(self):
        path = '/api/v1/games/info?name=vrkshop'
        response = self.client.get(path, headers=self.headers)
        print(response.get_data())
        assert response.status_code == 200

    def test_get_game_by_resource_unauthorized(self):
        path = '/api/v1/games/info?name=vrkshop'
        response = self.client.get(path, headers=self.wrong_headers)
        print(response.get_data())
        assert response.status_code == 401

    def test_update_game(self):
        path = '/api/v1/games'
        response = self.client.post(path, headers=self.headers, data=self.create_data)
        data = json.loads(response.get_data())
        game_id = data.get('insertedGameId')
        self.update_data['id_game'] = game_id
        response = self.client.put(path, headers=self.headers, data=json.dumps(self.update_data))
        print(response.get_data())
        assert response.status_code == 200

    def test_update_game_unauthorized(self):
        path = '/api/v1/games'
        response = self.client.put(path, headers=self.wrong_headers, data=json.dumps(self.update_data))
        print(response.get_data())
        assert response.status_code == 401
