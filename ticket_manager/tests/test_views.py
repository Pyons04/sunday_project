from datetime import datetime
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model

from ..models import Category, Status, User, Ticket

class LoadFixtures(TestCase):
  fixtures=['all.yaml']

  def test_login_sucess(self):
    """Fixtureで登録したユーザでログインを試行"""
    self.assertEqual(User.objects.count(), 1)

    self.client.login(username='user', password='user')
    response = self.client.get(reverse_lazy('list'))
    self.assertEqual(response.status_code, 200)

class TestCreateStatusView(TestCase):
  @classmethod
  def setUpClass(cls) -> None:

    super().setUpClass()
    cls.user = get_user_model().objects.create_user(
      username = 'test_status',
      password = 'test_status',
      email = 'test@test.com'
    )

  def test_create_status_fail(self):
    """ログインせずに上でステータスを作成しようとして失敗"""

    params = {
      'status':'新規',
      'order': 0
    }

    response = self.client.post(reverse_lazy('create_status'), params)
    self.assertEqual(response.status_code, 302)
    self.assertEqual(Status.objects.filter(status='新規',order=0).count(), 0)

  def test_create_status_success(self):
    """ログインした上でステータスを作成"""
    self.client.login(username='test_status', password='test_status')

    params = {
      'status':'新規',
      'order': 0
    }

    response = self.client.post(reverse_lazy('create_status'), params)
    self.assertRedirects(response, reverse_lazy('list'))
    self.assertEqual(Status.objects.filter(status='新規',order=0).count(), 1)

class TestCreateTicketView(TestCase):
  @classmethod
  def setUpClass(cls) -> None:

    super().setUpClass()
    cls.user = get_user_model().objects.create_user(
      username = 'test_ticket',
      password = 'test_ticket',
      email = 'test@test.com'
    )
      
    cls.status = Status.objects.create(
      status='新規',
      order=0
    )

    cls.category = Category.objects.create(
      category='Critical Incident'
    )

  def test_create_ticket_success(self):
    self.client.login(username='test_ticket', password='test_ticket')
    params = {
      'category' : self.category.id,
      'status'   : self.status.id,
      'title'    : 'Test Ticket',
      'description' : 'This is test ticket'
    }
    
    response = self.client.post(reverse_lazy('create'), params)
    self.assertRedirects(response, reverse_lazy('list'))
    self.assertEqual(Ticket.objects.filter(title='Test Ticket').count(), 1) 

  def test_create_ticket_with_enddate(self):
    self.client.login(username='test_ticket', password='test_ticket')
    params = {
      'category' : self.category.id,
      'status'   : self.status.id,
      'title'    : 'Test Ticket with Date',
      'description' : 'This is test ticket',
      'deadlinedate': '1996-10-10 00:00:00.000000+00:00'
    }

    response = self.client.post(reverse_lazy('create'), params)
    self.assertRedirects(response, reverse_lazy('list'))
    self.assertEqual(Ticket.objects.filter(deadlinedate=make_aware(datetime(1996,10,10))).count(), 1) 