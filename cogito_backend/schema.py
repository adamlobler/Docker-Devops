import graphene
import graphql_jwt

from .notes import schema
from .notes.schema.user import UserType


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info):
        return cls(user=info.context.user)


class Query(schema.Query, graphene.ObjectType):
    pass


class Mutations(schema.Mutations, graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
