from re import template
from django.shortcuts import render
from django.views import generic
from .models import Status, Ticket
from .forms  import StatusCreateForm, TicketCreateForm, LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import LoginForm # 追加

import logging
from django.urls import reverse_lazy
from django.contrib import messages

class KanbanView(LoginRequiredMixin, generic.ListView):
  model = Status
  template_name = 'kanban.html'

  def get_queryset(self):
      return Status.objects.order_by('order')

class CreateStatusView(LoginRequiredMixin, generic.CreateView):
  model = Status
  template_name = 'create_status.html'

  form_class = StatusCreateForm
  success_url = reverse_lazy('list')

  def form_valid(self, form):
    
    logger = logging.getLogger('development')
    logger.info('登録中')
    
    return super().form_valid(form)

class TicketView(LoginRequiredMixin, generic.ListView):
  model = Ticket
  template_name = 'list.html'

class CreateTicketView(LoginRequiredMixin, generic.CreateView):
  model = Ticket
  template_name = 'create.html'

  form_class = TicketCreateForm
  success_url = reverse_lazy('list')

  def form_valid(self, form):    
    logger = logging.getLogger('development')
    logger.info('登録中')
    
    return super().form_valid(form)
  
  def form_invalid(self, form):
    messages.error(self.request, "登録失敗")
    return super().form_invalid(form)

class UpdateTicketView(LoginRequiredMixin, generic.UpdateView):
  model = Ticket
  fields = ['status']
  template_name = 'ticket_update_form.html'
  success_url = reverse_lazy('kanban')

  def form_valid(self, form):    
    return super().form_valid(form)

class Login(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('kanban')

class Logout(LogoutView):
    template_name = 'logout.html'


