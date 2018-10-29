from django.db import models

from .socialbase import Social
from .snippet import Snippet
from .subject import Subject


class Note(models.Model):
    """
    A Cogito Note. Fields are self-explanatory.
    Use create() instead of constructor for instantiation.
    """
    author = models.ForeignKey('CogitoUser', on_delete=models.DO_NOTHING)
    social = models.OneToOneField(Social, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    noteType = models.CharField(max_length=128)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    @classmethod
    def create(self, user, noteType, title, initial_text):
        note_social = SocialBase()
        note_social.save()

        note = Note(id=None, author=user, noteType=noteType,
                    social=note_social, title=title)
        note.save()

        initial_ver = NoteVersion(text=initial_text, note=note)
        initial_ver.save()

        note.noteversion_set.add(initial_ver)

        return note

    @classmethod
    def delete(self, id):
        Note.objects.filter(id=id).delete()

    @property
    def text(self):
        return self.head.text

    @property
    def upvotes(self):
        return self.social.upvotes.count()

    @property
    def author(self):
        return self.author

    @property
    def created_at(self):
        return self.social.created_at

    def upvote(self, user):
        self.social.upvote(user)

    def unvote(self, user):
        self.social.unvote(user)

    def update(self, text):
        new_version = NoteVersion(text=text, note=self)
        new_version.save()

    def comment(self, user, text):
        self.social.comment(user, text)

    def __str__(self):
        return "Note: " + self.title
