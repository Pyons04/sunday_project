import imp
from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .models import Status

class TestCreateStatusView(TestCase):
  @classmethod
  def setUpClass(cls) -> None:

    super().setUpClass()
    cls.user = get_user_model().objects.create_user(
      username = 'test',
      password = 'test',
      email = 'test@test.com'
    )

  def test_create_status_success(self):
    self.client.login(username='test', password='test')

    params = {
      'status':'新規',
      'order': 0
    }

    response = self.client.post(reverse_lazy('create_status'), params)
    self.assertRedirects(response, reverse_lazy('list'))
    self.assertEqual(Status.objects.filter(status='新規',order=0).count(), 1)
# Create your tests here.
