# shim imghdr for Python 3.13 where stdlib imghdr is removed, required by python-telegram-bot 13.x
try:
    import imghdr  # type: ignore
except ModuleNotFoundError:
    import types
    import sys

    imghdr = types.ModuleType("imghdr")

    def what(filename, h=None):
        return None

    imghdr.what = what
    sys.modules["imghdr"] = imghdr

import logging
from typing import Dict, Any

from django.conf import settings
from telegram import Bot, Update
from telegram.ext import (
    CommandHandler,
    Dispatcher,
    Filters,
    MessageHandler,
)

from .handlers.commands import help_command, login, start
from .handlers.messages import contact_save, get_OTP_code

# Configure logging
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=4, use_context=True)

# Register handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("login", login))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(MessageHandler(Filters.contact, contact_save))
dispatcher.add_handler(
    MessageHandler(Filters.regex(r"^🔢 OTP kod olish$"), get_OTP_code)
)


def handle_update(data: Dict[str, Any]) -> None:
    """
    Processes incoming Telegram update from webhook.
    
    Args:
        data: Raw update data from Telegram API
    """
    try:
        update = Update.de_json(data, bot)
        if update:
            dispatcher.process_update(update)
        else:
            logger.warning("Received invalid update data")
    except Exception as e:
        logger.error(f"Error processing update: {e}")
