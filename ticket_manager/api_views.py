from yaml import serialize
from ticket_manager.models import Ticket
from ticket_manager.serializers import CategorySerializer, LoginSerializer, TicketSerializer

from django.contrib.auth import login, logout

from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

class TicketListCreateAPIView(views.APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request, *args, **kwargs):
    ticket_list = Ticket.objects.all()
    serialized = TicketSerializer(instance = ticket_list, many = True)
    return Response(serialized.data, status.HTTP_200_OK)

class TicketCreateAPIView(views.APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kwargs):
    pass

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

class CategoryCreateAPIView(views.APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kwargs):
    serialize = CategorySerializer(data=request.data)
    serialize.is_valid(raise_exception=True)
    serialize.save()
    return Response(serialize.data, status.HTTP_201_CREATED)