#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import os

token = os.getenv("TG_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle audio messages."""
    await update.message.reply_text("This message contains audio!")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo messages."""
    await update.message.reply_text("This message contains a photo!")


async def meta_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message)


async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle files."""
    document = update.message.document
    mime_type = document.mime_type
    if mime_type.startswith("image/"):
        await handle_photo(update, context)
    if mime_type.startswith("audio/"):
        await handle_audio(update, context)
    else:
        await meta_data(update, context)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # # on non command i.e message - echo the message on Telegram

    # Handle audio messages
    application.add_handler(MessageHandler(filters.AUDIO | filters.Document.AUDIO, handle_audio))

    # Handle voice messages
    application.add_handler(MessageHandler(filters.VOICE, handle_audio))

    # Handle photo messages
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_photo))

    # application.add_handler(MessageHandler(filters.Document.ALL, handle_files))


    # Handle all other types of messages
    custom_filter = ~filters.COMMAND & ~filters.AUDIO & ~filters.VOICE & ~filters.PHOTO & ~filters.Document.AUDIO & ~filters.Document.IMAGE
    application.add_handler(MessageHandler(custom_filter, meta_data))


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
