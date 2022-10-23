from django_filters import rest_framework as filters
from .models import Category, Status, Ticket

class CategoryFilter(filters.FilterSet):
  class Meta:
    model = Category
    fields = '__all__'

class TicketFilter(filters.FilterSet):
  class Meta:
    model = Ticket
    fields = '__all__'

class StatusFilter(filters.FilterSet):
  class Meta:
    model = Status
    fields = '__all__'
