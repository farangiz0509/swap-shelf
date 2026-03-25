import re
from random import randint
from typing import Any, Dict

from django.core.cache import cache
from rest_framework import serializers

from .models import User


class LoginSerializer(serializers.Serializer):
    """
    Serializer for initiating login by validating phone number and sending OTP.
    """
    phone_number = serializers.CharField()

    def validate_phone_number(self, value: str) -> str:
        # Normalize phone number to include + if not present
        if not value.startswith('+'):
            value = f'+{value}'
        
        pattern = r"^\+998\d{9}$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Telefon raqam '+998901234567' formatda bo'lishi kerak."
            )

        try:
            user = User.objects.get(phone=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Bunday telefon raqamiga ega foydalanuvchi topilmadi."
            )

        # Generate and cache OTP
        otp = str(randint(100000, 999999))
        cache_key = f"otp_{value}"
        
        if cache.get(cache_key):
            # OTP already sent recently
            otp = cache.get(cache_key)
        else:
            cache.set(cache_key, otp, timeout=300)  # 5 minutes
        
        # Send OTP via Telegram bot
        try:
            from ..bot.bot import bot
            bot.send_message(
                chat_id=user.telegram_id,
                text=f"🔐 Sizning SwapShelf uchun OTP kodingiz: `{otp}`\n\nBu kod 5 daqiqa amal qiladi.",
                parse_mode='Markdown'
            )
        except Exception as e:
            # Log error, but don't fail the request
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send OTP to user {user.id}: {e}")
        
        return value


class VerifySerializer(serializers.Serializer):
    """
    Serializer for verifying OTP and authenticating user.
    """
    phone_number = serializers.CharField()
    verify_code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        phone_number = attrs.get('phone_number')
        verify_code = attrs.get('verify_code')
        
        # Normalize phone number
        if not phone_number.startswith('+'):
            phone_number = f'+{phone_number}'
        
        pattern = r"^\+998\d{9}$"
        if not re.match(pattern, phone_number):
            raise serializers.ValidationError(
                {"phone_number": "Telefon raqam '+998901234567' formatda bo'lishi kerak."}
            )

        try:
            user = User.objects.get(phone=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"phone_number": "Bunday telefon raqamiga ega foydalanuvchi topilmadi."}
            )

        cache_key = f"otp_{phone_number}"
        cached_otp = cache.get(cache_key)
        
        if not cached_otp or cached_otp != verify_code:
            raise serializers.ValidationError(
                {"verify_code": "Yaroqsiz tekshirish kodi."}
            )

        # Clear OTP from cache
        cache.delete(cache_key)
        
        attrs['user'] = user
        return attrs
