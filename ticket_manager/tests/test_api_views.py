from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

class TestAuthFromAPI(APITestCase):

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.user = get_user_model().objects.create_user(
      username = 'test_auth_api',
      password = 'test_auth_api',
      email = 'test_auth@test.com'
    )

  def test_login(self):
    self.assertEqual(len(get_user_model().objects.all()),1)

    params = {
      'username':'test_auth_api',
      'password':'test_auth_api'
    }

    response = self.client.post('/ticket/api/login/', params, format='json')
    print(response)
    self.assertEqual(response.status_code, 200)
