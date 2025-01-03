from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from django.db import close_old_connections
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from rest_framework_simplejwt.exceptions import TokenError
from core.models._User import User

import logging

logger = logging.getLogger(__name__)

class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        if token:
            try:
                access_token = AccessToken(token)
                user = await self.get_user(access_token)
                scope['user'] = user
                logger.info(f"Authenticated WebSocket user: {user}")
            except Exception as e:
                logger.warning(f"WebSocket authentication failed: {e}")
                scope['user'] = AnonymousUser()
        else:
            logger.warning("No token provided in WebSocket query string.")
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, access_token):
        close_old_connections()
        user_id = access_token.get("user_id")
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.error(f"User with ID {user_id} not found.")
            return AnonymousUser()

async def __call__(self, scope, receive, send):
    query_string = parse_qs(scope["query_string"].decode())
    token = query_string.get("token", [None])[0]
    if token:
        try:
            access_token = AccessToken(token)
            user = await self.get_user(access_token)
            scope['user'] = user
        except TokenError as e:
            logger.warning(f"Invalid or expired token: {e}")
            scope['user'] = AnonymousUser()
        except Exception as e:
            logger.error(f"Unexpected error during token validation: {e}")
            scope['user'] = AnonymousUser()
    else:
        logger.warning("No token provided in WebSocket query string.")
        scope['user'] = AnonymousUser()

    return await super().__call__(scope, receive, send)
