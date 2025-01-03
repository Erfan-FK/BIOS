from django.db import models
from django.core.exceptions import ValidationError
from core.models._User import User

MESSAGE_TYPES = [
    ('broadcast', 'Broadcast Message'),
    ('direct', 'Direct Message'),
]

class Chat(models.Model):
    """Represents a one-to-one chat session between two users."""
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_participant1')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_participant2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.participant1.name} and {self.participant2.name}"

    def participants(self):
        """Returns both participants of the chat."""
        return [self.participant1, self.participant2]

    class Meta:
        unique_together = ['participant1', 'participant2']  # Ensure a unique pair of participants
        ordering = ['-created_at']


class Message(models.Model):
    """Represents a message sent in a chat or broadcasted."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    receivers = models.ManyToManyField(User, related_name='received_messages', blank=True)  # For broadcast messages
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='direct')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.ManyToManyField(User, related_name='seen_messages', blank=True)  # Track which users have seen the message

    def __str__(self):
        content_preview = (self.content[:30] + '...') if len(self.content) > 30 else self.content
        if self.message_type == 'direct' and self.chat:
            return f"Direct Message in Chat {self.chat.id}: {content_preview}"
        else:
            return f"Broadcast Message from {self.sender.name}: {content_preview}"

    def save(self, *args, **kwargs):
        if self.message_type == 'direct' and not self.chat:
            raise ValidationError("Direct messages must be associated with a chat.")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']
