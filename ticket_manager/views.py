from re import template
from django.shortcuts import render
from django.views import generic
from .models import Status, Ticket
from .forms  import StatusCreateForm, TicketCreateForm
import logging
import datetime
from django.urls import reverse_lazy
from django.contrib import messages

class CreateStatusView(generic.CreateView):
  model = Status
  template_name = 'create_status.html'

  form_class = StatusCreateForm
  success_url = reverse_lazy('list')

  def form_valid(self, form):
    #status = form.cleaned_data['status']
    #order = form.cleaned_data['order']
    
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
    created_date = datetime.datetime.now()
    title = form.cleaned_data['title']
    description = form.cleaned_data['description']
    
    logger = logging.getLogger('development')
    logger.info('登録中')
    
    #Ticket.objects.create(
    #  created_date=created_date,
    #  title=title,
    #  description=description,
    #)
    
    return super().form_valid(form)
  
  def form_invalid(self, form):
    messages.error(self.request, "登録失敗")
    return super().form_invalid(form)