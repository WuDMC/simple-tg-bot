from telegram import ForceReply, Update
from telegram.ext import ContextTypes
from telegram import Message
from data_processing import (
    get_download_url,
    download_and_encode_to_base64,
    detect_faces,
    save_audio
)

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
        await update.message.reply_text(f"This message contains a audio, lets save it to gdrive")
        file_id = await get_file_id(update.message)
        download_url = await get_download_url(file_id, context.bot.token)
        audio_result = await save_audio(download_url, update.message)
        await update.message.reply_text(f"Saving audio: {audio_result}")
    
    except ValueError as e:
        await update.message.reply_text(f"Error: {e}")




async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo messages."""
    try:
        await update.message.reply_text(f"This message contains a photo, lets try to detect faces")
        file_id = await get_file_id(update.message)
        download_url = await get_download_url(file_id, context.bot.token)
        image_64 = await download_and_encode_to_base64(download_url)
        faces_result = await detect_faces(image_64, update.message)
        await update.message.reply_text(f"Face detection: {faces_result}")
    
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
