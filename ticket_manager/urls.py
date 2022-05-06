from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.TicketView.as_view(), name="list"),
    path('create/', views.CreateTicketView.as_view(), name="create"),
    path('detail/<int:pk>/',views.TicketDetailView.as_view(), name ="detail"),
    path('update/<int:pk>/',views.UpdateTicketView.as_view(), name ="update"),
    path('status/', views.CreateStatusView.as_view(), name="create_status"),
    path('kanban/', views.KanbanView.as_view(), name="kanban"),
    path('ticket/<int:pk>/', views.UpdateStatusTicketView.as_view(), name="ticket_update")
]