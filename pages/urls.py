from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('faith/',views.faith,name='faith'),
    path('team/',views.team,name='team'),
    path('partners/',views.partners,name='partners'),
    path('giving/',views.giving,name='giving'),
    path('newsletter/',views.newsletter,name='newsletter'),
    path('activities/',views.activities,name='activities'),
    path('schedule/',views.schedule,name='schedule'),
    path('worship/',views.worship,name='worship'),

]