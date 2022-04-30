from django.shortcuts import render
from django.views import generic
from .models import Ticket
from .forms  import TicketCreateForm
import datetime
from django.urls import reverse_lazy

class TicketView(generic.ListView):
  model = Ticket
  template_name = 'list.html'

class CreateTicketView(generic.FormView):
  model = Ticket
  template_name = 'create.html'

  form_class = TicketCreateForm

  success_url = reverse_lazy('list')

  def form_valid(self, form):
    created_date = datetime.datetime.now()
    title = form.cleaned_data['title']
    description = form.cleaned_data['description']
    Ticket.objects.create(
      created_date=created_date,
      title=title,
      description=description,
    )
    return super().form_valid(form)



# Create your views here.
