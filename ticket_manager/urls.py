from django.urls import path
from . import views, api_views

urlpatterns = [
    # HTML Views
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('list/', views.TicketView.as_view(), name="list"),
    path('create/', views.CreateTicketView.as_view(), name="create"),
    path('detail/<int:pk>/',views.TicketDetailView.as_view(), name ="detail"),
    path('update/<int:pk>/',views.UpdateTicketView.as_view(), name ="update"),
    path('status/', views.CreateStatusView.as_view(), name="create_status"),
    path('kanban/', views.KanbanView.as_view(), name="kanban"),
    path('ticket/<int:pk>/', views.UpdateStatusTicketView.as_view(), name="ticket_update"),

    # API Views
    path('api/login/', api_views.LoginAPIView.as_view(), name="api_login"),
    path('api/logout/', api_views.LogoutAPIView.as_view(), name="api_logout"),
    path('api/list/', api_views.TicketListAPIView.as_view(), name="api_list"),
    path('api/category/', api_views.CategoryAPIView.as_view(), name='api_category'),
    path('api/category/<pk>/', api_views.CategoryAPIView.as_view(), name='api_category')
]