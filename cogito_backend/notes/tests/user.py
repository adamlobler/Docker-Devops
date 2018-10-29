from django.test import TestCase

from ..models.cogitouser import CogitoUser

class UserTest(TestCase):
    def test_create(self):
        adam = CogitoUser.objects.create(
            first_name="adam",
            last_name="lobler",
            email="adam.lobler@cogito.study"
        )
        adam.save()
        assert "adam lobler" == adam.__str__()