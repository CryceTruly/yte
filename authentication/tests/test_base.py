"""Base file containing setup"""


from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from authentication.models import User
from faker import Faker


class BaseTest(APITestCase):
    """Contains test setup method."""

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:login')
        self.registration_url = reverse('authentication:register')
        self.fake = Faker()

    def authenticate_user(self):
        user = User.objects.create_user(
            self.fake.email(), self.fake.email(), self.fake.password())
        user.is_verified = True
        user.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + user.token().get('access'))
