import json
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

class TestAuthFromAPI(APITestCase):
  fixtures=['all.yaml']

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.user = get_user_model().objects.create_user(
      username = 'test_auth_api',
      password = 'test_auth_api',
      email = 'test_auth@test.com'
    )

  def test_login(self):
    self.assertEqual(len(get_user_model().objects.all()),2)

    params = {
      'username':'test_auth_api',
      'password':'test_auth_api'
    }

    response = self.client.post('/ticket/api/login/', params, format='json')
    self.assertEqual(response.status_code, 200)

  # def test_get_ticket_list(self):
  #   params = {
  #     'username':'test_auth_api',
  #     'password':'test_auth_api'
  #   }

  #   response  = self.client.post('/ticket/api/login/', params, format='json')
  #   response2 = self.client.get('/ticket/api/list/'  , format='json')
  #   self.assertEqual(response2.status_code, 200)

  def test_get_ticket_list_fail(self):
    response = self.client.get('/ticket/api/list/'  ,format='json')
    self.assertEqual(response.status_code, 403)
    self.assertEqual(
      json.loads(response.content.decode('utf-8'))['detail'],
      'Authentication credentials were not provided.'
    )