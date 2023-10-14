from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('send_bitcoin/', views.send_bitcoin, name='send_bitcoin'),
    path('receive_bitcoin/', views.receive_bitcoin, name='receive_bitcoin'),
    path('submit_form/', views.submit_form, name='submit_form'),
]