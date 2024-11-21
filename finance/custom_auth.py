# Description: This file contains the middleware to check the token expiration time and renew the token if it is expired.

from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

class TokenExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            token = Token.objects.filter(user=request.user).first()
            if token:
                now = timezone.now()
                if (now - token.created) > timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS):
                    token.delete()
                    Token.objects.create(user=request.user)

        response = self.get_response(request)
        return response