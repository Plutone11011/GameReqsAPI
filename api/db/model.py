from marshmallow import Schema, fields, post_load, pre_load, validates, ValidationError

from api.utils.utils import convert_numeric_string, OPERATOR_URI_MAPPER


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

    def __str__(self):
        s = f'id {self.id_game}\n'
        s += f'name {self.name}\n'
        s += f'description {self.description}\n'
        s += f'ram {self.ram_min} {self.ram_rec}\n'
        s += f'cpu {self.cpu_min} {self.cpu_rec}\n'
        s += f'gpu {self.gpu_min} {self.gpu_rec}\n'
        s += f'OS {self.OS_min} {self.OS_rec}\n'
        s += f'storage {self.storage_min} {self.storage_rec}\n'
        return s


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
        ram_min_num = convert_numeric_string(data.get('ram_min'))
        storage_min_num = convert_numeric_string(data.get('storage_min'))
        ram_rec_num = convert_numeric_string(data.get('ram_rec'))
        storage_rec_num = convert_numeric_string(data.get('storage_rec'))

        data['ram_min'] = ram_min_num
        data['ram_rec'] = ram_rec_num
        data['storage_min'] = storage_min_num
        data['storage_rec'] = storage_rec_num

        return data

    @post_load
    def make_game(self, data, **kwargs):
        return Game(**data)


class UpdateGameSchema(GameSchema):
    id_game = fields.Integer(required=True)


class Filter:

    def __init__(self, op, memory, value):
        self.op = op
        self.memory = memory
        self.value = value


class FilterSchema(Schema):
    op = fields.Str(required=True)
    memory = fields.Str(required=True)
    value = fields.Float(required=True)

    @validates("op")
    def validate_op(self, val):
        if val not in OPERATOR_URI_MAPPER.keys():
            raise ValidationError("Op must be either one among eq, neq, gt, ge, le, lt")

    @validates("memory")
    def validate_memory(self, val):
        if val not in ["ram_min", "ram_rec", "storage_min", "storage_rec"]:
            raise ValidationError("Memory must be either one among ram_min, ram_rec, storage_min or storage_rec")

    @post_load
    def make_filter(self, data, **kwargs):
        return Filter(**data)


class Page():

    def __init__(self, last_id, limit):
        self.last_id = last_id
        self.limit = limit


class PageSchema(Schema):
    last_id = fields.Integer(required=True)
    limit = fields.Integer(required=True)

    @post_load
    def make_filter(self, data, **kwargs):
        return Page(**data)