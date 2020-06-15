from marshmallow import Schema, fields, post_load, pre_load

from api.utils.utils import convert_numeric_string


class Game:

    def __init__(self, id_game, name, description, developer, ram_min, cpu_min, gpu_min, OS_min, storage_min,
                 ram_rec, cpu_rec, gpu_rec, OS_rec, storage_rec):
        self.id_game = id_game
        self.name = name
        self.description = description
        self.developer = developer
        self.ram_min = ram_min
        self.cpu_min = cpu_min
        self.gpu_min = gpu_min
        self.OS_min = OS_min
        self.storage_min = storage_min
        self.ram_rec = ram_rec
        self.cpu_rec = cpu_rec
        self.gpu_rec = gpu_rec
        self.OS_rec = OS_rec
        self.storage_rec = storage_rec


class GameSchema(Schema):
    id_game = fields.Integer(missing=None)
    name = fields.Str(required=True)
    description = fields.Str(missing=None)
    developer = fields.Str(missing=None)
    ram_min = fields.Float(missing=None)
    cpu_min = fields.Str(missing=None)
    gpu_min = fields.Str(missing=None)
    OS_min = fields.Str(missing=None)
    storage_min = fields.Float(missing=None)
    ram_rec = fields.Float(missing=None)
    cpu_rec = fields.Str(missing=None)
    gpu_rec = fields.Str(missing=None)
    OS_rec = fields.Str(missing=None)
    storage_rec = fields.Float(missing=None)

    @pre_load
    def convert_numerics(self, data, **kwargs):
        ram_min_num = convert_numeric_string(data['ram_min'])
        storage_min_num = convert_numeric_string(data['storage_min'])
        ram_rec_num = convert_numeric_string(data['ram_rec'])
        storage_rec_num = convert_numeric_string(data['storage_rec'])

        data['ram_min'] = ram_min_num
        data['ram_rec'] = ram_rec_num
        data['storage_min'] = storage_min_num
        data['storage_rec'] = storage_rec_num

        return data

    @post_load
    def make_game(self, data, **kwargs):
        print(data)
        return Game(**data)
