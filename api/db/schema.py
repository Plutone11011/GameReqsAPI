from marshmallow import Schema, fields


class InfoSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    developer = fields.Str()


class MinimumRequirementsSchema(Schema):
    ram = fields.Float()
    cpu = fields.Str()
    gpu = fields.Str()
    os = fields.Str()
    storage = fields.Float()


class RecommendedRequirementsSchema(Schema):
    ram = fields.Float()
    cpu = fields.Str()
    gpu = fields.Str()
    os = fields.Str()
    storage = fields.Float()


class GameSchema(Schema):
    info = fields.Nested(InfoSchema)
    minimum_req = fields.Nested(MinimumRequirementsSchema)
    recommended_req = fields.Nested(RecommendedRequirementsSchema)
