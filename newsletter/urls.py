from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('', views.NewsletterArchiveView.as_view(), name='archive'),
    path('<slug:slug>/', views.NewsletterDetailView.as_view(), name='detail'),
]