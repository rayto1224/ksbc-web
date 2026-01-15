from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('', views.UpcomingEventsListView.as_view(), name='list'),
    path('<int:event_id>/', views.EventDetailView.as_view(), name='detail'),
    path('<int:event_id>/register/', views.EventRegistrationCreateView.as_view(), name='register'),
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('withdraw/<int:registration_id>/', views.WithdrawRegistrationView.as_view(), name='withdraw'),
]
