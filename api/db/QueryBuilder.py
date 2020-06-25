import pypika

from api.db.model import Page
from api.utils.utils import OPERATOR_URI_MAPPER

class GameQueryBuilder:

    def __init__(self, *args):
        self.game = pypika.Table('Games')
        self.query_builder = pypika.SQLLiteQuery.from_(self.game).select(*args if args else '*')
        self.params = {
            'where_params': [],
            'limit_params': [],
            # might add more
        }

    def name_query(self, name: str):
        self.query_builder = self.query_builder.where(self.game.name == pypika.Parameter(' ? '))
        name = name.replace('"', '', 2)
        self.params['where_params'].append(name)

    def pagination_query(self, page: Page):
        self.query_builder = self.query_builder.where(self.game.id > pypika.Parameter(' ? ')).limit(pypika.Parameter(' ? '))
        self.params['where_params'].append(page.last_id)
        self.params['limit_params'].append(page.limit)

    def filter_query(self, filters):

        for filter in filters:
            self.query_builder = self.query_builder.where(OPERATOR_URI_MAPPER[filter.op](pypika.Parameter(filter.memory), pypika.Parameter(' ? ')))
            self.params['where_params'].append(filter.value)

    def param_builder(self):
        return self.params['where_params'] + self.params['limit_params']

