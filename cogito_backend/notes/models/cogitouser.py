from functools import reduce

from django.db import models
from django.contrib.auth.models import AbstractUser

from .note import Note
from .snippet import Snippet
from .comment import Comment


class CogitoUser(AbstractUser):
    """
    Custom Cogito user, left empty for future extending. Also used in Auth model.
    """

    userRole = models.CharField(max_length=128)
    is_admin = models.BooleanField()

    @classmethod
    def create(self, first_name, last_name, email, password, userTypeName, userDisplayName, admin=False):
        user = CogitoUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            userRole=userTypeName,
            is_admin=admin
        )
        user.set_password(password)
        user.save()
        return user

    @property
    def notes(self):
        return Note.objects.filter(social__author__id=self.id)

    @property
    def snippets(self):
        return Snippet.objects.filter(social__author__id=self.id)

    @property
    def comments(self):
        return Comment.objects.filter(social__author__id=self.id)

    @property
    def upvotes(self):
        return reduce(lambda acc, curr: acc + curr.upvotes, self.notes, 0) + \
            reduce(lambda acc, curr: acc + curr.upvotes, self.snippets, 0) + \
            reduce(lambda acc, curr: acc + curr.upvotes, self.comments, 0)

    def __str__(self):
        return self.first_name + " " + self.last_name
