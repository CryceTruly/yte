"""user login tests"""
from .test_base import BaseTest
from rest_framework.views import status
from .test_data import valid_user, valid_login


class UserLoginTest(BaseTest):

    """Contains user login test methods."""

    def test_inactivated_user_cannot_login(self):
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.post(self.login_url, valid_login, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
