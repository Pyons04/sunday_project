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
    """
    認証に成功 
    """
    self.assertEqual(len(get_user_model().objects.all()),2)

    params = {
      'username':'test_auth_api',
      'password':'test_auth_api'
    }

    response = self.client.post('/ticket/api/login/', params, format='json')
    # csrf_tokenの取得を確認
    self.assertTrue(response.cookies['csrftoken'])
    self.assertEqual(response.status_code, 200)

  def test_login_failed(self):
    """
    認証に失敗
    """
    params = {
      'username':'test_auth_api',
      'password':'invalid_password'
    }

    response  = self.client.post('/ticket/api/login/', params, format='json')
    # csrf_tokenの取得失敗を確認
    with self.assertRaises(KeyError):
      response.cookies['csrftoken']
    self.assertEqual(response.status_code, 403) #FIXME: 本来401が返るべき
    self.assertEqual(
      json.loads(response.content.decode('utf-8'))['detail'],
      'Login Failed'
    )

  def test_get_ticket_list(self):
    """
    認証に成功し、その後チケット一覧を要求して成功
    """
    params = {
      'username':'test_auth_api',
      'password':'test_auth_api'
    }

    response = self.client.post('/ticket/api/login/', params, format='json')
    response = self.client.get('/ticket/api/ticket/',params  , format='json')
    self.assertEqual(response.status_code, 200)

  def test_get_ticket_list_fail(self):
    """
    認証を経由せず、チケット一覧を要求して失敗
    """
    response = self.client.get('/ticket/api/ticket/'  ,format='json')
    
    self.assertEqual(response.status_code, 403)

    self.assertEqual(
      json.loads(response.content.decode('utf-8'))['detail'],
      'Authentication credentials were not provided.'
    )