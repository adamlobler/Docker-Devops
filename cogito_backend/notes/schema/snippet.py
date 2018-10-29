import graphene
from graphene_django import DjangoObjectType

from .user import UserType
from .note import NoteType
from .comment import CommentType

from ..models.cogitouser import CogitoUser
from ..models.snippet import Snippet

class SnippetType(DjangoObjectType):
    user = graphene.Field(UserType)
    note = graphene.Field(NoteType)
    comments = graphene.List(CommentType)
    upvotes = graphene.Int()
    

    class Meta: model = Snippet

    def resolve_user(self, info):
        return self.author
    
    def resolve_upvotes(self, info):
        return self.upvotes
    
    def resolve_comments(self, info):
        return self.comments
    
    def resolve_note(self, info):
        return self.note

class SnippetQueries(graphene.ObjectType):
    snippets = graphene.List(SnippetType)
    snippet = graphene.Field(SnippetType, id=graphene.Int())

    def resolve_snippets(self, info):
        return Snippet.objects.all()
    
    def resolve_snippet(self, info, id):
        return Snippet.objects.get(id=id)

class DeleteSnippet(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        snippet_id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, user_id, snippet_id):
        snippet = Snippet.objects.get(pk=snippet_id)
        if snippet.author.pk == user_id or snippet.note.author.id == user_id:
            Snippet.delete(snippet_id)
            return DeleteSnippet(success=True)
        return DeleteSnippet(success=False)

class MergeSnippet(graphene.Mutation): # Needs real implementation
    class Arguments:
        user_id = graphene.Int()
        snippet_id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, user_id, snippet_id):
        snippet = Snippet.objects.get(pk=snippet_id)
        if snippet.note.author.id == user_id:
            snippet.merge()
            return MergeSnippet(success=True)
        return MergeSnippet(success=False)

class CommentSnippet(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        snippet_id = graphene.Int()
        text = graphene.String()

    snippet = graphene.Field(SnippetType)
    success = graphene.Boolean()

    def mutate(self, info, user_id, snippet_id, text):
        snippet = Snippet.objects.get(pk=snippet_id)
        user = CogitoUser.objects.get(pk=user_id)
        snippet.add_comment(user, text)
        return CommentSnippet(success=True, snippet=snippet)

class UpvoteSnippet(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        snippet_id = graphene.Int()

    success = graphene.Boolean()
    snippet = graphene.Field(SnippetType)

    def mutate(self, info, user_id, snippet_id):
        snippet = Snippet.objects.get(pk=snippet_id)
        user = CogitoUser.objects.get(pk=user_id)
        snippet.upvote(user)
        return UpvoteSnippet(success=True, snippet=snippet)

class UnvoteSnippet(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        snippet_id = graphene.Int()

    success = graphene.Boolean()
    snippet = graphene.Field(SnippetType)

    def mutate(self, info, user_id, snippet_i):
        snippet = Snippet.objects.get(pk=snippet_id)
        user = CogitoUser.objects.get(pk=user_id)
        snippet.unvote(user)
        return UnvoteSnippet(success=True, snippet=snippet)

class SnippetMutations(graphene.ObjectType):
    delete_snippet = DeleteSnippet.Field()
    merge_snippet = MergeSnippet.Field()
    comment_snippet = CommentSnippet.Field()
    upvote_snippet = UpvoteSnippet.Field()
    unvote_snippet = UnvoteSnippet.Field()
