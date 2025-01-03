from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.messaging._Message import Message
from core.messaging.serializer import MessageSerializer, ChatSerializer
from django.db.models import Q
from core.models._User import User
from core.messaging._Message import Chat
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        data = request.data
        message_type = data.get('message_type')

        if message_type == 'direct':
            chat_id = data.get('chat_id')
            content = data.get('content')
            if not chat_id or not content:
                return Response({"error": "Chat ID and content are required for direct messages."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                chat = Chat.objects.get(id=chat_id)
                if sender not in [chat.participant1, chat.participant2]:
                    return Response({"error": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)
                message = Message.objects.create(sender=sender, chat=chat, message_type='direct', content=content)

                # Notify WebSocket group
                channel_layer = get_channel_layer()
                serializer = MessageSerializer(message, context={'request': request})
                async_to_sync(channel_layer.group_send)(
                    f"user_{chat.participant1.id}",  # Notify participant1
                    {"type": "chat_message", "message": serializer.data}
                )
                async_to_sync(channel_layer.group_send)(
                    f"user_{chat.participant2.id}",  # Notify participant2
                    {"type": "chat_message", "message": serializer.data}
                )
            except Chat.DoesNotExist:
                return Response({"error": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

        elif message_type == 'broadcast':
            receivers = data.get('receivers')
            content = data.get('content')
            if not receivers or not content:
                return Response({"error": "Receivers and content are required for broadcast messages."}, status=status.HTTP_400_BAD_REQUEST)
            message = Message.objects.create(sender=sender, message_type='broadcast', content=content)
            message.receivers.set(User.objects.filter(id__in=receivers))

            # Notify WebSocket broadcast group
            channel_layer = get_channel_layer()
            serializer = MessageSerializer(message, context={'request': request})
            async_to_sync(channel_layer.group_send)(
                "broadcast",  # Broadcast to the 'broadcast' group
                {"type": "chat_message", "message": serializer.data}
            )
        else:
            return Response({"error": "Invalid message type."}, status=status.HTTP_400_BAD_REQUEST)

        response_data = MessageSerializer(message, context={'request': request}).data
        return Response({"message": "Message sent successfully", "data": response_data}, status=status.HTTP_201_CREATED)


class RetrieveMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Query messages
        received_messages = Message.objects.filter(receivers=user).order_by('-timestamp')  # Optional: Order by timestamp
        sent_messages = Message.objects.filter(sender=user).order_by('-timestamp')  # Optional: Order by timestamp
        unseen_count = received_messages.exclude(is_seen=user).count()

        # Serialize data without pagination
        data = {
            "received_messages": MessageSerializer(received_messages, many=True, context={'request': request}).data,
            "sent_messages": MessageSerializer(sent_messages, many=True, context={'request': request}).data,
            "unseen_count": unseen_count
        }

        return Response(data, status=status.HTTP_200_OK)


class DeleteMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id, sender=request.user)
            message.delete()
            return Response({"message": "Message deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response({"error": "Message not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)


class EditMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id, sender=request.user)
            new_content = request.data.get('content')
            if not new_content:
                return Response({"error": "Content cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
            message.content = new_content
            message.save()
            return Response({"message": "Message updated successfully", "data": MessageSerializer(message, context={'request': request}).data}, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response({"error": "Message not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)


class CreateChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        contact_id = request.data.get('contact_id')
        if not contact_id:
            return Response({"error": "Contact ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            contact = User.objects.get(id=contact_id)
            if contact == user:
                return Response({"error": "Cannot create a chat with yourself."}, status=status.HTTP_400_BAD_REQUEST)
            existing_chat = Chat.objects.filter(
                Q(participant1=user, participant2=contact) |
                Q(participant1=contact, participant2=user)
            ).first()
            if existing_chat:
                return Response(ChatSerializer(existing_chat, context={'request': request}).data, status=status.HTTP_200_OK)
            chat = Chat.objects.create(participant1=user, participant2=contact)
            return Response(ChatSerializer(chat, context={'request': request}).data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class ListChatsForUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        # If user_id is not provided, use the logged-in user
        user = request.user if not user_id else User.objects.filter(id=user_id).first()

        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all chats where the user is a participant
        chats = Chat.objects.filter(
            Q(participant1=user) | Q(participant2=user)
        )
        include_messages = request.query_params.get('include_messages', 'false').lower() == 'true'
        serializer_context = {'request': request, 'include_messages': include_messages}
        serializer = ChatSerializer(chats, many=True, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RetrieveChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        try:
            # Get the chat by ID
            chat = Chat.objects.get(id=chat_id)

            # Ensure the requesting user is a participant in the chat
            if request.user not in [chat.participant1, chat.participant2]:
                return Response({"error": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)

            # Include messages in the response
            include_messages = request.query_params.get('include_messages', 'true').lower() == 'true'
            serializer_context = {'request': request, 'include_messages': include_messages}

            # Serialize the chat with or without messages
            serializer = ChatSerializer(chat, context=serializer_context)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Chat.DoesNotExist:
            return Response({"error": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)
        
class MarkMessagesAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        user = request.user

        if chat_id == 'broadcast':
            # For broadcast messages
            messages = Message.objects.filter(
                message_type='broadcast',
                receivers=user,
            ).exclude(is_seen=user)
        else:
            # For direct messages
            chat = get_object_or_404(Chat, id=chat_id)
            if user not in [chat.participant1, chat.participant2]:
                return Response(
                    {"error": "You are not a participant in this chat."},
                    status=status.HTTP_403_FORBIDDEN
                )
            messages = Message.objects.filter(
                chat=chat
            ).exclude(is_seen=user)

        # Mark each message as seen by the user
        for message in messages:
            message.is_seen.add(user)

        return Response(
            {"message": "Messages marked as read."},
            status=status.HTTP_200_OK
        )