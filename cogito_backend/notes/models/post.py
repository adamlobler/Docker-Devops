from django.db import models
from django.utils import timezone

from .cogitouser import CogitoUser
from .socialbase import SocialBase
from .subject import Subject


class Post(models.Model):
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(CogitoUser, on_delete=models.DO_NOTHING)
    content = models.CharField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    social = models.OneToOneField(SocialBase, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(editable=True)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Post, self).save(*args, **kwargs)
