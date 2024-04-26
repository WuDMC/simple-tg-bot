from telegram.ext import Updater, MessageHandler, Filters
from telegram import Update
import os

token = os.getenv("TG_BOT_TOKEN")

# Функция-обработчик текстовых сообщений
def handle_text(update: Update, context):
    update.message.reply_text("Вы отправили текстовое сообщение")

# Функция-обработчик аудио сообщений
def handle_audio(update: Update, context):
    update.message.reply_text("Вы отправили аудио")

# Функция-обработчик фото сообщений
def handle_photo(update: Update, context):
    update.message.reply_text("Вы отправили фото")

# Функция-обработчик остальных типов сообщений
def handle_other(update: Update, context):
    update.message.reply_text("Вы отправили другой тип сообщения")

def main():
    # Создаем Updater и передаем ему токен бота
    updater = Updater(token, use_context=True)

    # Получаем dispatcher для регистрации обработчиков
    dp = updater.dispatcher

    # Регистрируем обработчики для различных типов сообщений
    dp.add_handler(MessageHandler(Filters.text, handle_text))
    dp.add_handler(MessageHandler(Filters.audio, handle_audio))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(MessageHandler(~(Filters.text | Filters.audio | Filters.photo), handle_other))

    # Запускаем бота
    updater.start_polling()

    # Бот работает до принудительной остановки
    updater.idle()

if __name__ == '__main__':
    main()
