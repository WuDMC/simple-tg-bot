#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.


import logging

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from handlers import (
    start,
    help_command,
    echo,
    handle_audio,
    handle_photo,
    meta_data,
    handle_files,
)

import os

token = os.getenv("TG_BOT_TOKEN")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def run_bot() -> None:
    """Start the bot."""
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Handle audio messages
    application.add_handler(
        MessageHandler(filters.AUDIO | filters.Document.AUDIO, handle_audio)
    )

    # Handle voice messages
    application.add_handler(MessageHandler(filters.VOICE, handle_audio))

    # Handle photo messages
    application.add_handler(
        MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_photo)
    )

    # Handle all other types of messages
    custom_filter = (
        ~filters.COMMAND
        & ~filters.AUDIO
        & ~filters.VOICE
        & ~filters.PHOTO
        & ~filters.Document.AUDIO
        & ~filters.Document.IMAGE
    )
    application.add_handler(MessageHandler(custom_filter, meta_data))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    run_bot()
