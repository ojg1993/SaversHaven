from django.urls import path

from . import views

urlpatterns = [
    path('rooms/', views.ChatRoomListCreateView.as_view(), name='chat_rooms'),
    path('rooms/<int:room_id>/', views.MessageListView.as_view(), name='chat_messages'),
]
