
class Info:

    def __init__(self, name, description, developer):
        self.name = name
        self.description = description
        self.developer = developer


class MinimumRequirements:

    def __init__(self, ram, cpu, gpu, os, storage):
        self.ram = ram
        self.cpu = cpu
        self.gpu = gpu
        self.os = os
        self.storage = storage


class RecommendedRequirements:

    def __init__(self, ram, cpu, gpu, os, storage):
        self.ram = ram
        self.cpu = cpu
        self.gpu = gpu
        self.os = os
        self.storage = storage


class Game:

    def __init__(self, info: Info, minimum_req: MinimumRequirements, recommended_req: RecommendedRequirements):
        self.info = info
        self.minimum_req = minimum_req
        self.recommended_req = recommended_req
