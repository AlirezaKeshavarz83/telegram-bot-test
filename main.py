import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def code(update, context):
    update.message.reply_text(update.message.chat.id)

updater = Updater("1729081335:AAFTRl8eBQ8wZ79-1Lw7Yi1vd8vXVuiKHJE", use_context=True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("code", code))

updater.start_polling()

updater.idle()
