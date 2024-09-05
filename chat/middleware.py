import logging
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])

        # Debugging: Print the headers
        logging.debug(f"Headers: {headers}")

        if b'authorization' in headers:
            auth_header = headers[b'authorization'].decode('utf-8')
            logging.debug(f"Auth Header: {auth_header}")

            token_name, token = auth_header.split()

            if token_name.lower() == 'bearer':
                try:
                    # Decode the token and get the user ID
                    decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                    logging.debug(f"Decoded Token: {decoded_data}")

                    user = await get_user(decoded_data["user_id"])
                    logging.debug(f"User from token: {user}")

                    scope['user'] = user
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
                    logging.error(f"JWT Error: {str(e)}")
                    scope['user'] = AnonymousUser()
        else:
            logging.debug("No Authorization header found")
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)
