import imp
from django.test import TestCase
from django.urls import reverse_lazy

from .models import Status

class TestCreateStatusView(TestCase):
  def test_create_status_success(self):
    params = {
       'status':'新規',
       'order': 0
     }

    response = self.client.post(reverse_lazy('create_status'), params)
    self.assertRedirects(response, reverse_lazy('list'))
    self.assertEqual(Status.objects.filter(status='新規',order=0).count(), 1)
# Create your tests here.
