from django.dispatch import Signal
from django.contrib.auth import get_user_model


message_sent = Signal(providing_args=["message"])