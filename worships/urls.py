from django.urls import path
from . import views

app_name = 'worships'

urlpatterns = [
    path('', views.worships_page, name='worships'),   # ← MAIN PAGE
    path('api/sermons/', views.sermons_api, name='sermons_api'),
]
