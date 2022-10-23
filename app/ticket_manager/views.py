from .models import Status, Ticket, Category
from .forms  import StatusCreateForm, TicketCreateForm, TicketUpdateForm, LoginForm

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

import logging
from django.urls import reverse_lazy

from django.db.models import Q

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

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['status_list'] = Status.objects.all();
    context['category_list'] = Category.objects.all();
    return context
  
  def get_queryset(self):
    q_word = self.request.GET.get('query')
    q_category = self.request.GET.get('category')
    q_status = self.request.GET.get('status')
 
    if q_word:
      object_list = Ticket.objects.filter(
            Q(title__icontains=q_word) | Q(description__icontains=q_word))
    else:
      object_list = Ticket.objects.all()
    
    if q_category:
      object_list = object_list.filter(Q(category=q_category))
    
    if q_status:
      object_list = object_list.filter(Q(status=q_status))
      
    return object_list

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
    return super().form_invalid(form)

class UpdateStatusTicketView(generic.UpdateView):
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

class TicketDetailView(generic.DetailView):
  model = Ticket
  template_name = 'detail.html'

class UpdateTicketView(generic.UpdateView):
  model = Ticket
  template_name = 'update.html'
  form_class = TicketUpdateForm
  success_url = reverse_lazy('list')

  def form_valid(self, form):    
    return super().form_valid(form)

  def form_invalid(self, form):
    return super().form_invalid(form)


