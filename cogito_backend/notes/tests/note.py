from django.test import TestCase

from ..models.note import Note
from ..models.cogitouser import CogitoUser

class NoteTest(TestCase):
    def setUp(self):
        adam = CogitoUser.objects.create(
            first_name="adam",
            last_name="lobler",
            email="adam.lobler@cogito.study"
        )
        adam.save()
        self.user = adam

        note = Note.create(
            self.user,
            "Számítógépes grafika",
            "Mi az a vertexbuffer?"
        )
        note.save()
        self.note = note
    
    def test_upvote(self):
        self.note.upvote(self.user)
        assert self.note.upvotes == 1

    def test_unvote(self):
        self.note.unvote(self.user)
        assert self.note.upvotes == 0

    def test_add_snippet(self):
        self.note.add_snippet(self.user)
        assert self.note.snippet_set.count() == 1

    def test_update(self):
        new_content = """Mi az a vertexbuffer?
A vertex buffer object (VBO) is an OpenGL \
feature that provides methods for uploading\
 vertex data (position, normal vector, color,\
  etc.) to the video device for non-immediate-mode\
   rendering. VBOs offer substantial performance\
    gains over immediate mode rendering primarily\
     because the data resides in the video device\
      memory rather than the system memory and so\
       it can be rendered directly by the video device.\
        These are equivalent to vertex buffers in Direct3D."""
        
        self.note.update(new_content)

        assert self.note.noteversion_set.count() == 2
        assert self.note.text == new_content