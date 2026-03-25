from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from ..bot.services.user_services import get_or_create_user
from .serializers import LoginSerializer, VerifySerializer


class TelegramWebhookView(APIView):
    """
    Handles incoming updates from Telegram Bot API via webhook.
    """
    def post(self, request: Request) -> Response:
        from ..bot.bot import handle_update

        data = request.data
        handle_update(data)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    """
    Initiates login process by sending OTP to user's phone via Telegram.
    """
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Tekshirish kodi Telegramdan yuborildi."},
            status=status.HTTP_200_OK
        )


class TokenVerifyView(APIView):
    """
    Verifies OTP and issues JWT tokens for authenticated user.
    """
    def post(self, request: Request) -> Response:
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "phone": user.phone,
                    "rating": user.rating,
                }
            },
            status=status.HTTP_200_OK
        )
