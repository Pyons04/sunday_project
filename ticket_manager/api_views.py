from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from yaml import serialize
from ticket_manager.models import Ticket, Category, Status
from ticket_manager.serializers import CategorySerializer, LoginSerializer, StatusSerializer, TicketSerializer

from django.contrib.auth import login, logout

from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import CategoryFilter, TicketFilter
from django_filters import rest_framework as filters

class TicketListAPIView(views.APIView):
  permission_classes = [IsAuthenticated]
  
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

class CategoryAPIView(views.APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kwargs):
    serialize = CategorySerializer(data=request.data)
    serialize.is_valid(raise_exception=True)
    serialize.save()
    return Response(serialize.data, status.HTTP_201_CREATED)

  def get(self, request, *args, **kwargs):
    filterset = CategoryFilter(request.query_params, queryset=Category.objects.all())
    if not filterset.is_valid():
      raise ValidationError(filterset.errors)
    serialize = CategorySerializer(instance=filterset.qs, many=True)
    return Response(serialize.data, status.HTTP_200_OK)

  def patch(self, request, pk, *args, **kwargs):
    category = get_object_or_404(Category, pk=pk)
    serialize = CategorySerializer(instance=category, data=request.data, partial=True)
    serialize.is_valid(raise_exception=True)
    serialize.save()
    return Response(serialize.data, status.HTTP_200_OK)

class TicketDetailAPIView(views.APIView):
  permission_classes = [IsAuthenticated]
  filter_backends = [filters.DjangoFilterBackend]
  filterset_fields = '__all__'

  def get(self, request, pk, *args, **kwargs):
    ticket = get_object_or_404(Ticket, pk=pk)
    serialize = TicketSerializer(instance = ticket)
    return Response(serialize.data, status.HTTP_200_OK)

class TicketAPIView(views.APIView):
  permission_classes = [IsAuthenticated]
  filter_backends = [filters.DjangoFilterBackend]
  filterset_fields = '__all__'

  def get(self, request, *args, **kwargs):
    filterset = TicketFilter(request.query_params, queryset=Ticket.objects.all())
    if not filterset.is_valid():
      raise ValidationError(filterset.errors)
    serialize = TicketSerializer(instance=filterset.qs, many=True)
    return Response(serialize.data, status.HTTP_200_OK)

  def post(self, request, *args, **kwargs):
    serialize = TicketSerializer(data=request.data)
    serialize.is_valid(raise_exception=True)
    serialize.save()
    return Response(serialize.data, status.HTTP_201_CREATED)

  def patch(self, request, pk, *args, **kwargs):
    ticket = get_object_or_404(Ticket, pk=pk)
    serialize = TicketSerializer(instance=ticket, data=request.data, partial=True)
    serialize.is_valid(raise_exception=True)
    serialize.save()
    return Response(serialize.data, status.HTTP_200_OK)

class StatusAPIView(views.APIView):
  permission_classes = [IsAuthenticated]
  filter_backends = [filters.DjangoFilterBackend]
  filterset_fields = '__all__'

  def get(self, request, pk, *args, **kwargs):
    status_obj = get_object_or_404(Status, pk=pk)
    serialize = StatusSerializer(instance = status_obj)
    return Response(serialize.data, status.HTTP_200_OK)

  def post(self, request, *args, **kwargs):
    serialize = StatusSerializer(data=request.data)
    serialize.is_valid(raise_exception=True)
    serialize.save()
    return Response(serialize.data, status.HTTP_201_CREATED)

  def patch(self, request, pk, *args, **kwargs):
    status_obj = get_object_or_404(Status, pk=pk)
    serialize = StatusSerializer(instance=status_obj, data=request.data, partial=True)
    serialize.is_valid(raise_exception=True)
    serialize.save()
    return Response(serialize.data, status.HTTP_200_OK)

