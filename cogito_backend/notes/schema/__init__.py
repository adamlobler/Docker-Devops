import graphene
import graphql_jwt


from .comment import CommentQueries, CommentMutations
from .note import NoteQueries, NoteMutations
from .snippet import SnippetQueries, SnippetMutations
from .user import UserType, UserQueries, UserMutations


class Query(
    CommentQueries,
    NoteQueries,
    SnippetQueries,
    UserQueries
):
    pass


class Mutations(
    CommentMutations,
    NoteMutations,
    UserMutations,
    SnippetMutations,
):
    pass
