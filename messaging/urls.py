from django.urls import path
from . import views

urlpatterns = [
    path('send_message/', views.send_message, name='send_message'),
    path('messages/', views.messages, name='messages'),
    path('chat/<str:receiver_address>/', views.chat, name='chat'),
    path('api/send_message/<str:receiver_address>/', views.send_message_api, name='send_message_api'),
]
