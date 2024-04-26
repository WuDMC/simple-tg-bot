from telegram import ForceReply, Update
from telegram.ext import ContextTypes


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
