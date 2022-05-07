from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('list/', views.TicketView.as_view(), name="list"),
    path('create/', views.CreateTicketView.as_view(), name="create"),
    path('status/', views.CreateStatusView.as_view(), name="create_status"),
    path('kanban/', views.KanbanView.as_view(), name="kanban"),
    path('ticket/<int:pk>/', views.UpdateTicketView.as_view(), name="ticket_update")
]