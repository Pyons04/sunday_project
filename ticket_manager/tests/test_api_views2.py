from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
import json

class TestCRUD(APITestCase):

  params = {
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
    

  def test_crud_category(self):

    response = self.client.post('/ticket/api/login/', self.params, format='json')

    # Create
    category = {
      'category' : "APIテストカテゴリ"
    }
    response = self.client.post('/ticket/api/category/', category, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    id = json.loads(response.content.decode('utf-8'))['id']

    # Update
    category_update = {
      'category' : "APIテストカテゴリUpdate"
    }
    response2 = self.client.patch('/ticket/api/category/' + str(id) + '/', category_update, format='json')
    self.assertEqual(response2.status_code, status.HTTP_200_OK)

    # List
    response3 = self.client.get('/ticket/api/category/?id=' + str(id), format='json')
    self.assertEqual(response3.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response3.content.decode('utf-8'))[0]['category'], 'APIテストカテゴリUpdate')

    # Delete
    response4 = self.client.delete('/ticket/api/category/' + str(id) + '/', format='json')
    self.assertEqual(response4.status_code, status.HTTP_204_NO_CONTENT)








    