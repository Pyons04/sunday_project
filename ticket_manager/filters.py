from django_filters import rest_framework as filters
from .models import Category, Ticket

class CategoryFilter(filters.FilterSet):
  class Meta:
    model = Category
    fields = '__all__'

class TicketFilter(filters.FilterSet):
  class Meta:
    model = Ticket
    fields = '__all__'
