from rest_framework import serializers
from core.models._User import User
from core.messaging._Message import Message
from core.messaging._Message import Chat
from django.db import models

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model to include profile picture, name, and role."""
    class Meta:
        model = User
        fields = ['id', 'name', 'profile_picture', 'role']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Include detailed sender info
    receivers = UserSerializer(many=True, read_only=True)  # Include detailed receiver info
    is_seen = serializers.SerializerMethodField()  # Check if the message is seen
    chat = serializers.PrimaryKeyRelatedField(read_only=True)  # Include chat ID

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'receivers',
            'chat',
            'message_type',
            'content',
            'timestamp',
            'is_seen',
        ]

    def get_is_seen(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user in obj.is_seen.all()
        return False

    def validate(self, data):
        """Ensure direct messages have a chat."""
        if data.get('message_type') == 'direct' and not data.get('chat'):
            raise serializers.ValidationError("Direct messages must be associated with a chat.")
        return data


class SendMessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = MessageSerializer()


class RetrieveMessagesResponseSerializer(serializers.Serializer):
    received_messages = MessageSerializer(many=True)
    sent_messages = MessageSerializer(many=True)
    unseen_count = serializers.IntegerField()  # Include unseen messages count


class ChatSerializer(serializers.ModelSerializer):
    participant1 = UserSerializer(read_only=True)
    participant2 = UserSerializer(read_only=True)
    messages = serializers.SerializerMethodField()  # Include optional messages

    class Meta:
        model = Chat
        fields = ['id', 'participant1', 'participant2', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at']

    def get_messages(self, obj):
        """Include messages in the chat if requested."""
        if self.context.get('include_messages'):
            messages = obj.messages.all().order_by('-timestamp')
            return MessageSerializer(messages, many=True, context=self.context).data
        return None

    def validate(self, data):
        """
        Ensure that participant1 and participant2 are not the same user and that the chat is unique.
        """
        participant1 = self.context['request'].user
        participant2 = data.get('participant2')
        if participant1 == participant2:
            raise serializers.ValidationError("A user cannot chat with themselves.")
        
        # Check if chat already exists
        if Chat.objects.filter(
            models.Q(participant1=participant1, participant2=participant2) |
            models.Q(participant1=participant2, participant2=participant1)
        ).exists():
            raise serializers.ValidationError("Chat between these users already exists.")
        
        return data
