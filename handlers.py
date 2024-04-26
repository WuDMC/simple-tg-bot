from telegram import ForceReply, Update
from telegram.ext import ContextTypes
from telegram import Message

import requests


async def get_file_id(message: Message) -> str:
    """Get the file ID from a Telegram message."""
    if message.audio:
        return message.audio.file_id
    elif message.voice:
        return message.voice.file_id
    elif message.document:
        return message.document.file_id
    elif message.photo:
        # Assuming the first photo in the array is the largest size
        return message.photo[-1].file_id
    else:
        raise ValueError("Message does not contain supported file type")


async def get_download_url(file_id: str, bot_token: str) -> str:
    """Get the download URL for a file with the given file_id."""
    try:
        # Construct the API request URL to get file information
        file_info_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
        
        # Send the request to get file information
        response = requests.get(file_info_url)
        response.raise_for_status()  # Raise an error for bad response status
        
        file_info = response.json()['result']  # Extract the result containing file information
        file_path = file_info['file_path']  # Get the file_path from the file information
        
        # Construct the URL for downloading the file
        download_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        return download_url
    
    except (requests.RequestException, KeyError) as e:
        raise ValueError(f"Error occurred while getting download URL: {e}")

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
    try:
        file_id = await get_file_id(update.message)
        download_url = await get_download_url(file_id, context.bot.token)
        await update.message.reply_text(f"This message contains a audio! You can download it from:\n{download_url}")
    
    except ValueError as e:
        await update.message.reply_text(f"Error: {e}")




async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo messages."""
    try:
        file_id = await get_file_id(update.message)
        download_url = await get_download_url(file_id, context.bot.token)
        await update.message.reply_text(f"This message contains a photo! You can download it from:\n{download_url}")
    
    except ValueError as e:
        await update.message.reply_text(f"Error: {e}")



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
