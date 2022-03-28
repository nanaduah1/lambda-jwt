import graphene

from auth.models import User


class UserObject(graphene.ObjectType):
    username = graphene.String()
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    id = graphene.Int()
    groups = graphene.List(graphene.String)

    def resolve_groups(user, info):
        return user.permissions


class UserQuery(graphene.ObjectType):
    users = graphene.List(UserObject)

    def resolve_users(p, info):
        return User.select()
