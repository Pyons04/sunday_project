from django.shortcuts import render
from django.views import generic
from .models import Ticket
from .forms  import TicketCreateForm

class TicketView(generic.ListView):
  model = Ticket
  template_name = 'list.html'

class CreateTicketView(generic.CreateView):
  model = Ticket
  template_name = 'create.html'

  form_class = TicketCreateForm

  def form_valid(self, form):
    ticket = form.save(commit=True)
    ticket.save()

    logger = logging.getLogger('development')
    logger.info('登録中')

    messages.success(self.request, "登録完了")
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, "登録失敗")
    return super().form_invalid(form)



# Create your views here.
