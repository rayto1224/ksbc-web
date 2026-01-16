
from django.urls import path
from . import views

app_name = 'worships'
urlpatterns = [
    path('worship/',views.sermon_list,name='worship'),
    path('api/sermons/', views.get_sermons, name='get_sermons'),
    #path('', views.sermon_list, name='sermon_list'),  # Changed to empty path
]