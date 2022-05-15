from re import template
from django.shortcuts import render
from django.views import generic
from yaml import serialize

from ticket_manager.serializers import LoginSerializer, TicketSerializer
from .models import Status, Ticket, Category
from .forms  import StatusCreateForm, TicketCreateForm, LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms  import StatusCreateForm, TicketCreateForm, TicketUpdateForm
import logging
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout

from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


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
    messages.error(self.request, "更新失敗")
    return super().form_invalid(form)

class TicketListCreateAPIView(LoginRequiredMixin, views.APIView):
  def get(self, request, *args, **kwargs):
    ticket_list = Ticket.objects.all()
    serialized = TicketSerializer(instance = ticket_list, many = True)
    return Response(serialized.data, status.HTTP_200_OK)

class LoginAPIView(generics.GenericAPIView):
  serializer_class = LoginSerializer
  permission_classes = [AllowAny]

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception = True)
    user = serializer.validated_data['user']
    login(request, user)
    return Response({
      'detailed' : 'ログインに成功しました'
    })

class LogoutAPIView(views.APIView):
  def post(self, request, *args, **kwargs):
    logout(request)
    return Response({
      'detailed' : 'ログアウトに成功しました'
    })



