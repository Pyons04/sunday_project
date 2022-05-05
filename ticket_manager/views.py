from re import template
from django.shortcuts import render
from django.views import generic
from .models import Status, Ticket
from .forms  import StatusCreateForm, TicketCreateForm
import logging
import datetime
from django.urls import reverse_lazy
from django.contrib import messages

class KanbanView(generic.ListView):
  model = Status
  template_name = 'kanban.html'

  def get_queryset(self):
      return Status.objects.order_by('order')
  

class CreateStatusView(generic.CreateView):
  model = Status
  template_name = 'create_status.html'

  form_class = StatusCreateForm
  success_url = reverse_lazy('list')

  def form_valid(self, form):
    
    logger = logging.getLogger('development')
    logger.info('登録中')
    
    return super().form_valid(form)

class TicketView(generic.ListView):
  model = Ticket
  template_name = 'list.html'

class CreateTicketView(generic.CreateView):
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

class UpdateTicketView(generic.UpdateView):
  model = Ticket
  fields = ['status']
  template_name = 'ticket_update_form.html'
  success_url = reverse_lazy('kanban')

