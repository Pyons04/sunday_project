from django.shortcuts import render
from django.views import generic
from .models import Ticket
from .forms  import TicketCreateForm
import logging
import datetime
from django.urls import reverse_lazy
from django.contrib import messages

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
    
    messages.success(self.request, "登録完了")
    
    return super().form_valid(form)
  
  def form_invalid(self, form):
    messages.error(self.request, "登録失敗")
    return super().form_invalid(form)