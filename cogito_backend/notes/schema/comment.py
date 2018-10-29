import graphene
from graphene_django import DjangoObjectType

from .user import UserType

from ..models.comment import Comment
from ..models.cogitouser import CogitoUser


class CommentType(DjangoObjectType):
    user = graphene.Field(UserType)
    replies = graphene.List(lambda: CommentType)
    upvotes = graphene.Int()

    class Meta:
        model = Comment

    def resolve_user(self, info):
        return self.author

    def resolve_replies(self, info):
        return self.children.all()

    def resolve_upvotes(self, info):
        return self.upvotes


class CommentQueries(graphene.ObjectType):
    comments = graphene.List(CommentType)
    comment = graphene.Field(CommentType)

    def resolve_comments(self, info):
        return Comment.objects.all()

    def resolve_comment(self, info, id):
        return Comment.objects.get(id=id)


class EditComment(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        comment_id = graphene.Int()
        text = graphene.String()

    comment = graphene.Field(CommentType)
    success = graphene.Boolean()

    def mutate(self, info, user_id, comment_id, text):
        comment = Comment.objects.get(pk=comment_id)
        if comment.author.pk == user_id:
            comment.edit(text)
            return EditComment(success=True, comment=comment)
        return EditComment(success=False, comment=None)


class DeleteComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.Int()
        user_id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, comment_id, user_id):
        comment = Comment.objects.get(pk=comment_id)
        if comment.author.pk == user_id:
            Comment.delete(comment_id)
            return DeleteComment(success=True)
        return DeleteComment(success=False)


class ReplyComment(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        comment_id = graphene.Int()
        text = graphene.String()

    reply = graphene.Field(CommentType)
    success = graphene.Boolean()

    def mutate(self, info, user_id, comment_id, text):
        comment = Comment.objects.get(pk=comment_id)
        user = CogitoUser.objects.get(pk=user_id)
        comment.add_reply(user, text)
        return ReplyComment(reply=comment, success=True)


class UpvoteComment(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        comment_id = graphene.Int()

    success = graphene.Boolean()
    comment = graphene.Field(CommentType)

    def mutate(self, info, user_id, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        user = CogitoUser.objects.get(pk=user_id)
        comment.upvote(user)
        return UpvoteComment(success=True, comment=comment)


class UnvoteComment(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        comment_id = graphene.Int()

    success = graphene.Boolean()
    comment = graphene.Field(CommentType)

    def mutate(self, info, user_id, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        user = CogitoUser.objects.get(pk=user_id)
        comment.unvote(user)
        return UnvoteComment(success=True, comment=comment)


class CommentMutations(graphene.ObjectType):
    edit_comment = EditComment.Field()
    delete_comment = DeleteComment.Field()
    reply_comment = ReplyComment.Field()
    upvote_comment = UpvoteComment.Field()
    unvote_comment = UnvoteComment.Field()
