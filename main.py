from telegram.ext import Updater, CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from googletrans import Translator
from settings import *

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

TEXT, LANGUAGE = 0, 1


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Salom botga xush kelibsiz.Tarjima qilish uchun textni yuboring")
    return TEXT


def text_to_translate(update: Update, context: CallbackContext):
    text = update.message.text
    languages = ['uz', 'en', 'ru']
    buttons = [[KeyboardButton(language) for language in languages]]
    reply_buttons = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("Kerakli tilni tanlang", reply_markup=reply_buttons)
    context.user_data['text'] = text
    return LANGUAGE


def translator(update: Update, context: CallbackContext):
    language = update.message.text
    text = context.user_data['text']
    tarjimon = Translator()
    tarjima = tarjimon.translate(text, dest=language).text
    update.message.reply_text(f"Tarjima qilingan text:{tarjima}\n"
                              f"Yana text tarjima qilish uchun /start buyrug'idan foydalaning")
    # return start(update, context)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={TEXT: [MessageHandler(Filters.text, text_to_translate)],
            LANGUAGE: [MessageHandler(Filters.regex("^(uz|en|ru)$"), translator)]},
    fallbacks=[],
)
dispatcher = updater.dispatcher
dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()
