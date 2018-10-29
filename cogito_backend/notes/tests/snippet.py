from django.test import TestCase

from ..models.snippet import Snippet
from ..models.note import Note
from ..models.cogitouser import CogitoUser

class SnippetTest(TestCase):
    def setUp(self):
        adam = CogitoUser.objects.create(
            first_name="adam",
            last_name="lobler",
            email="adam.lobler@cogito.study"
        )
        adam.save()
        self.user = adam

        note = Note.create(adam, "Graphics", "I love Computer Graphics")
        note.save()
        self.note = note

        self.note.add_snippet(adam)
        self.snippet = self.note.snippet_set.first()

    def test_delete(self):
        pk = self.snippet.pk
        Snippet.delete(pk)
        assert Snippet.objects.filter(pk=pk).count() == 0
        assert self.note.snippet_set.count() == 0

    def test_comment(self):
        self.snippet.add_comment(self.user, "Great suggestion!")
        assert self.snippet.social.comment.children.first().text == "Great suggestion!"

    def test_upvote(self):
        self.snippet.upvote(self.user)
        assert self.snippet.social.upvotes.count() == 1


    def test_upvote(self):
        self.snippet.unvote(self.user)
        assert self.snippet.social.upvotes.count() == 0

    def merge(self):
        self.snippet.merge()
        assert snippet.merged == True