from django.db import models

from .socialbase import Social
from .comment import Comment


class Snippet(models.Model):
    """
    A Snippet from the text of a Note.
    Refer to Cogito Notes Editing Draft for further info on Note structure.
    Use create() insted of constructor for instantiation.
    Snippet already saved before returning from function.
    """

    social = models.OneToOneField(Social, on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE)
    merged = models.BooleanField(default=False)

    @classmethod
    def create(self, user, note):
        snippet_social = SocialBase(author=user)
        snippet_social.save()

        snippet = Snippet(social=snippet_social, note=note)
        snippet.social.comment = Comment.create(
            user, user.first_name + " created this snippet")
        snippet.social.comment.save()
        snippet.save()

        return snippet

    @classmethod
    def delete(self, id):
        Snippet.objects.filter(id=id).delete()

    @property
    def upvotes(self):
        return self.social.upvotes.count()

    @property
    def author(self):
        return self.social.author

    @property
    def comments(self):
        return self.social.comment.children.all()

    def merge(self):
        self.merged = True
        self.save()

    def upvote(self, user):
        if not self.merged:
            self.social.upvote(user)

    def unvote(self, user):
        if not self.merged:
            self.social.unvote(user)

    def add_comment(self, user, text):
        if not self.merged:
            self.social.comment.add_reply(user, text)
