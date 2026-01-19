from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('faith/',views.faith,name='faith'),
    path('team/',views.team,name='team'),
    path('partners/',views.partners,name='partners'),
    path('giving/',views.giving,name='giving'),
    path('',views.index,name='index'),
]