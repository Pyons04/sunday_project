from datetime import datetime, timedelta, tzinfo
import imp
from time import timezone
from unicodedata import category
import zoneinfo
from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .models import Category, Status, User, Ticket

class LoadFixtures(TestCase):
  fixtures=['all.yaml']

  def test_login_sucess(self):
    """Fixtureで登録したユーザでログインを試行して成功"""

    self.assertEqual(User.objects.count(), 1)

    self.client.login(username='user', password='user')
    response = self.client.get(reverse_lazy('list'))
    self.assertEqual(response.status_code, 200)

class TestKanbanView(TestCase):
  fixtures=['all.yaml']

  @classmethod
  def setUpClass(cls) -> None:

    super().setUpClass()
    cls.user = get_user_model().objects.create_user(
      username = 'test_kanban',
      password = 'test_kanban',
      email = 'test@test.com'
    )

  def test_update_status_from_kanban(self):
    """カンバンボードからチケットのステータスを更新"""
    self.client.login(username='test_kanban', password='test_kanban')

    params = {
      'status' : 2
    }

    response = self.client.post(reverse_lazy('ticket_update',kwargs={'pk': 1}), params)
    self.assertEqual(response.status_code, 302)
    self.assertEqual(Ticket.objects.get(id=1).status.id, 2)

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
    """期限なしのチケットを発行して成功"""
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
    """期限有のチケットを発行して成功"""
    self.client.login(username='test_ticket', password='test_ticket')
    params = {
      'category' : self.category.id,
      'status'   : self.status.id,
      'title'    : 'Test Ticket with Date',
      'description' : 'This is test ticket',
      'deadlinedate': '1996-10-10'
    }

    response = self.client.post(reverse_lazy('create'), params)
    self.assertRedirects(response, reverse_lazy('list'))

    time_with_tzinfo = datetime(
      1996,
      10,
      10,
      tzinfo=zoneinfo.ZoneInfo(key='UTC')
    )
    self.assertEqual(Ticket.objects.filter(deadlinedate=time_with_tzinfo).count(), 1) 