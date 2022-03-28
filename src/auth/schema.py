import graphene

from auth.mutations import AuthMutation
from auth.queries import UserQuery


class Query(UserQuery):
    pass


class Mutations(AuthMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=True)
