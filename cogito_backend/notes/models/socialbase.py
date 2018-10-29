from django.db import models


class Social(models.Model):
    """
    Encapsulates all the social features (upvotes, created-at date, author, comments) of a Cogito business object.
    """

    created_at = models.DateTimeField(auto_now_add=True)

    upvotes = models.ManyToManyField(
        'CogitoUser', related_name='upvoted', blank=True)

    def upvote(self, user):
        if user not in self.upvotes.all():
            self.upvotes.add(user)

    def unvote(self, user):
        if user in self.upvotes.all():
            self.upvotes.remove(user)

    def add_reply(self, user, text):
        self.comment.comment(user, text)
