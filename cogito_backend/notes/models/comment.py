from django.db import models

from .socialbase import Social


class Comment(models.Model):
    """
    A comment. Fields are self-explanatory
    """

    social = models.OneToOneField(Social, on_delete=models.CASCADE)
    text = models.TextField()
    edited = models.BooleanField(default=False)

    parent = models.ForeignKey(
        'Comment',
        related_name='children',
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    @classmethod
    def create(self, user, text):
        comment_social = SocialBase(author=user)
        comment_social.save()

        comment = Comment(text=text, social=comment_social)
        comment.save()

        return comment

    @classmethod
    def delete(self, id):
        Comment.objects.filter(id=id).delete()

    @property
    def upvotes(self):
        return self.social.upvotes.count()

    @property
    def author(self):
        return self.social.author

    def upvote(self, user):
        self.social.upvote(user)

    def unvote(self, user):
        self.social.unvote(user)

    def add_reply(self, user, text):
        reply = Comment.create(user, text)
        reply.save()
        self.children.add(reply)

    def edit(self, new_text):
        self.edited = True
        self.text = new_text
        self.save()

    def __str__(self):
        return "Comment: " + self.text + "..."
