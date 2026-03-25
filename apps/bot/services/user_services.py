from typing import Optional

from ...users.models import User


def get_or_create_user(
    telegram_id: int,
    first_name: str,
    last_name: str,
    username: Optional[str],
    phone: Optional[str] = None
) -> str:
    """
    Gets or creates a user based on Telegram data.
    
    Returns a status message.
    """
    user, created = User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'name': f"{first_name} {last_name}".strip(),
            'telegram_username': username,
            'phone': phone,
        }
    )
    
    if created:
        return "foydalanuvchi topilmadi, yangi foydalanuvchi yaratildi"
    elif user.phone is None:
        return "telefon raqami kiritilmagan"
    else:
        return "hamma malumotlar to'liq, foydalanuvchi topildi"


def set_webhook(url: str) -> None:
    """
    Sets the webhook URL for the Telegram bot.
    
    Args:
        url: The webhook URL to set
    """
    # Implementation would go here
    pass
