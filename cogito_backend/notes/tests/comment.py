from django.test import TestCase

from ..models.comment import Comment
from ..models.cogitouser import CogitoUser

class CommentTest(TestCase):
    def setUp(self):
        adam = CogitoUser.objects.create(
            first_name="adam",
            last_name="lobler",
            email="adam.lobler@cogito.study"
        )
        adam.save()
        self.user = adam

        comment = Comment.create(self.user, "Technology follows design")
        comment.save()
        self.comment = comment
    
    def test_upvote(self):
        self.comment.upvote(self.user)
        assert self.comment.upvotes == 1

    def test_unvote(self):
        self.comment.unvote(self.user)
        assert self.comment.upvotes == 0

    def test_add_reply(self):
        self.comment.add_reply(self.user, "- Steve Jobs")
        assert self.comment.children.first().text == "- Steve Jobs"

    def test_edit(self):
        self.comment.edit("Technology follows technology")
        assert self.comment.text == "Technology follows technology"

    def test_delete(self):
        pk = self.comment.pk
        Comment.delete(self.comment.pk)
        assert Comment.objects.filter(pk=pk).count() == 0



    