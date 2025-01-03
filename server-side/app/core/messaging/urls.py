from django.urls import path
from core.messaging.view import (
    SendMessageView,
    RetrieveMessagesView,
    DeleteMessageView,
    EditMessageView,
    CreateChatView,
    ListChatsForUserView,
    RetrieveChatView,
    MarkMessagesAsReadView,  # Import the new view
)

urlpatterns = [
    path('messages/send/', SendMessageView.as_view(), name='message_send'),
    path('messages/', RetrieveMessagesView.as_view(), name='message_list'),
    path('messages/<int:message_id>/delete/', DeleteMessageView.as_view(), name='message_delete'),
    path('messages/<int:message_id>/edit/', EditMessageView.as_view(), name='message_edit'),
    path('chats/', CreateChatView.as_view(), name='chat_create'),
    path('chats/<int:user_id>/', ListChatsForUserView.as_view(), name='chat_list_for_contact'),
    path('chats/<int:chat_id>/details/', RetrieveChatView.as_view(), name='chat_details'),
    path('chats/<str:chat_id>/mark-read/', MarkMessagesAsReadView.as_view(), name='mark_messages_as_read'),  # New URL
]