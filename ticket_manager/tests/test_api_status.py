from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
import json

class TestAPIStatus(APITestCase):

  login_info = {
      'username':'test_auth_api',
      'password':'test_auth_api'
  }

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.user = get_user_model().objects.create_user(
      username = 'test_auth_api',
      password = 'test_auth_api',
      email = 'test_auth@test.com'
    )

  def test_crud_status(self):
    response = self.client.post('/ticket/api/login/', self.login_info, format='json')

    # Create
    status_param = {
      'status' : "APIテストステータス",
      'order'  : '5.0'
    }
    response = self.client.post('/ticket/api/status/', status_param, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    id = json.loads(response.content.decode('utf-8'))['id']

    # Update
    status_update = {
      'status' : "APIテストステータスUpdate"
    }
    response2 = self.client.patch('/ticket/api/status/' + str(id) + '/', status_update, format='json')
    self.assertEqual(response2.status_code, status.HTTP_200_OK)

    # List
    response3 = self.client.get('/ticket/api/status/?id=' + str(id) , format='json')
    self.assertEqual(response3.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response3.content.decode('utf-8'))[0]['status'], 'APIテストステータスUpdate')

    # Delete
    response4 = self.client.delete('/ticket/api/status/' + str(id) + '/', format='json')
    self.assertEqual(response4.status_code, status.HTTP_204_NO_CONTENT)
