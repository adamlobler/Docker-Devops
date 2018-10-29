from django.db import models


class Subject(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=128)
    semester = models.IntegerField()
    description = models.TextField()
    prerequisites = models.ForeignKey('Subject', on_delete=models.DO_NOTHING)
