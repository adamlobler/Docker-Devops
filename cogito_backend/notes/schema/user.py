import graphene
from graphene_django import DjangoObjectType

from ..models.cogitouser import CogitoUser


class UserType(DjangoObjectType):
    upvotes = graphene.Int()

    class Meta:
        model = CogitoUser

    def resolve_upvotes(self, info):
        print(info.context.user)
        return self.upvotes


class UserQueries(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_users(self, info):
        return CogitoUser.objects.all()

    def resolve_user(self, info, id):
        return CogitoUser.objects.get(id=id)


class CreateUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()  # TODO: Validation
        password = graphene.String()  # TODO: Validation

    success = graphene.Boolean()
    user = graphene.Field(UserType)

    def mutate(self, info, first_name, last_name, email, password):
        user = CogitoUser.create(first_name, last_name, email, password)
        success = True
        return CreateUser(user=user, success=success)


class UserMutations(graphene.ObjectType):
    create_user = CreateUser.Field()
