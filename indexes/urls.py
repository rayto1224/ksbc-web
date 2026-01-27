# indexes/urls.py
from django.urls import path
from . import views

app_name = "indexes"

urlpatterns = [
    path("", views.home_page, name="home"),  # 首页
    path("ministry/<int:ministry_id>/", views.ministry_details, name="ministry"),
]
