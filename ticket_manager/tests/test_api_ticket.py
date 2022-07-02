import json
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

class TestAPIAuth(APITestCase):
  fixtures=['test_api_ticket.yaml']
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
    ticket_param = {
      'status' : '999',
      'category'  : '999',
      'title' : 'テストAPIチケット',
      'description' : 'このチケットはAPIから作成されました',
    }

    response = self.client.post('/ticket/api/ticket/', ticket_param, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    id = json.loads(response.content.decode('utf-8'))['id']

    # Update
    ticket_update = {
      'description' : "APIテストチケットUpdate"
    }
    response2 = self.client.patch('/ticket/api/ticket/' + str(id) + '/', ticket_update, format='json')
    self.assertEqual(response2.status_code, status.HTTP_200_OK)

    # Get(query)
    response3 = self.client.get('/ticket/api/ticket/?id=' + str(id), format='json')
    self.assertEqual(response3.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response3.content.decode('utf-8'))[0]['description'], 'APIテストチケットUpdate')

    # Get(pk)
    response4 = self.client.get('/ticket/api/ticket/' + str(id) + '/', format='json')
    self.assertEqual(response4.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response4.content.decode('utf-8'))['description'], 'APIテストチケットUpdate')

    # Delete
    response4 = self.client.delete('/ticket/api/ticket/' + str(id) + '/', format='json')
    self.assertEqual(response4.status_code, status.HTTP_204_NO_CONTENT)

  def test_delete_protect(self):
    """
    Ticketオブジェクトに外部キーとして紐づいているオブジェクトが削除出来ないことを確認。
    """
    response = self.client.post('/ticket/api/login/', self.login_info, format='json')

    # Create
    ticket_param = {
      'status' : '999',
      'category'  : '999',
      'title' : 'テストAPIチケット',
      'description' : 'このチケットはAPIから作成されました',
    }

    response = self.client.post('/ticket/api/ticket/', ticket_param, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    response2 = self.client.delete('/ticket/api/status/999/', format='json')
    self.assertEqual(response2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    response3 = self.client.delete('/ticket/api/category/999/', format='json')
    self.assertEqual(response3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    self.assertEqual(json.loads(response3.content.decode('utf-8'))['message'], 'リソースの削除に失敗しました。')






