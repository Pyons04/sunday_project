from django.shortcuts import render
from django.views import generic
from .models import Ticket
from .forms  import TicketCreateForm

class TicketView(generic.ListView):
  model = Ticket
  template_name = 'list.html'

class CreateTicketView(generic.FormView):
  model = Ticket
  template_name = 'create.html'

  form_class = TicketCreateForm



# Create your views here.
