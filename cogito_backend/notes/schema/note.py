import graphene
from graphene_django import DjangoObjectType

from .user import UserType
from .comment import CommentType

from ..models.cogitouser import CogitoUser
from ..models.note import Note


class NoteType(DjangoObjectType):
    user = graphene.Field(UserType)
    upvotes = graphene.Int()
    text = graphene.String()
    created_at = graphene.Date()

    class Meta:
        model = Note

    def resolve_user(self, info):
        return self.author

    def resolve_text(self, info):
        return self.text

    def resolve_upvotes(self, info):
        return self.upvotes

    def resolve_created_at(self, info):
        return self.created_at


class NoteQueries(graphene.ObjectType):
    notes = graphene.List(NoteType)
    note = graphene.Field(NoteType, id=graphene.Int())
    notes_of_user = graphene.List(NoteType, userId=graphene.Int())

    def resolve_notes(self, info):
        return Note.objects.all()

    def resolve_note(self, info, id):
        return Note.objects.get(id=id)

    def resolve_notes_of_user(self, info, userId):
        return Note.objects.filter(social__author__id=userId)


class CreateNote(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        title = graphene.String()

    note = graphene.Field(NoteType)
    success = graphene.Boolean()

    def mutate(self, info, user_id, title):
        user = CogitoUser.objects.get(pk=user_id)
        note = Note.create(user, title, EMPTY_NOTE)
        return CreateNote(note=note, success=True)


class EditNote(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        note_id = graphene.Int()
        text = graphene.String()

    note = graphene.Field(NoteType)
    success = graphene.Boolean()

    def mutate(self, info, user_id, note_id, text):
        user = CogitoUser.objects.get(pk=user_id)
        note = Note.objects.get(pk=note_id)
        if note.author.pk == user_id:
            note.update(text)
            return EditNote(note=note, success=True)
        return EditNote(note=None, success=False)


class NoteMutations(graphene.ObjectType):
    create_note = CreateNote.Field()
    add_snippet_to_note = AddSnippetToNote.Field()
    edit_note = EditNote.Field()


EMPTY_NOTE = """{
    "document": {
      "nodes": [
        {
          "object": "block",
          "type": "heading-one",
          "nodes": [
            {
              "object": "text",
              "leaves": [
                {
                  "text": "New Note"
                }
              ]
            }
          ]
        },
        {
          "object": "block",
          "type": "paragraph",
          "nodes": [
            {
              "object": "text",
              "leaves": [
                {
                  "text": ""
                }
              ]
            }
          ]
        }
      ]
    }
  }"""
