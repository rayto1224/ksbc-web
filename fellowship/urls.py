from django.urls import path
from .views import fellowship_page

app_name = "fellowship"

urlpatterns = [
    path("", fellowship_page, name="fellowship"),
]
