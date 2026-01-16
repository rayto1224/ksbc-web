from django.urls import path
from . import views

app_name = "fellowship"

urlpatterns = [
    path('fellowship/',views.fellowship_page,name='fellowship'),
]
