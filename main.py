import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

chat_dogs = {}

def start(update, context):
    global chat_dogs
    try:
        chat_dogs[update.message.chat.id]
    except:
        chat_dogs[update.message.chat.id] = []
    user = update.message.from_user
    try:
        msg_cnt = int(context.args[0])
    except:
        msg_cnt = 50
    try:
        user = update.message.reply_to_message.from_user
    except:
        user = update.message.from_user
    for dog in chat_dogs[update.message.chat.id]:
        if(dog[0] == user):
            dog[1] = msg_cnt
            dog[2] = 0
            update.message.reply_text("Updated dog <a href=\"tg://user?id=" + str(user.id) + "\">" + user.first_name + "</a> : \n msg_cnt = " + str(msg_cnt), parse_mode="HTML")
            return
    chat_dogs[update.message.chat.id] += [[user, msg_cnt, 0]]
    update.message.reply_text("Added dog <a href=\"tg://user?id=" + str(user.id) + "\">" + user.first_name + "</a> : \n msg_cnt = " + str(msg_cnt), parse_mode="HTML")
    #update.message.reply_text(update.message.reply_to_message.from_user.id)

def end(update, context):
    global chat_dogs
    try:
        chat_dogs[update.message.chat.id]
    except:
        chat_dogs[update.message.chat.id] = []
    user = update.message.from_user
    try:
        user = update.message.reply_to_message.from_user
    except:
        user = update.message.from_user
    for dog in chat_dogs[update.message.chat.id]:
        if(dog[0] == user):
            chat_dogs[update.message.chat.id].remove(dog)
            update.message.reply_text("Removed dog <a href=\"tg://user?id=" + str(user.id) + "\">" + user.first_name + "</a>", parse_mode="HTML")
            return
    update.message.reply_text("<a href=\"tg://user?id=" + str(user.id) + "\">" + user.first_name + "</a> is not a dog", parse_mode="HTML")
def count(update, context):
    global chat_dogs
    try:
        chat_dogs[update.message.chat.id]
    except:
        chat_dogs[update.message.chat.id] = []
    user = update.message.from_user
    if user.is_bot:
        return
    for dog in chat_dogs[update.message.chat.id]:
        dog[2] += 1
        if(dog[0] == user):
            dog[2] = 0
        if(dog[2] == dog[1]):
            update.message.reply_text("Dog found: <a href=\"tg://user?id=" + str(dog[0].id) + "\">" + dog[0].first_name + "</a>\nMessage Count: " + str(dog[1]), parse_mode="HTML")
            dog[2] = 0
def stats(update, context):
    global chat_dogs
    try:
        chat_dogs[update.message.chat.id]
    except:
        chat_dogs[update.message.chat.id] = []
    if(len(chat_dogs[update.message.chat.id]) == 0):
        update.message.reply_text("No dogs!😃", parse_mode="HTML")
        return
    msg = "Dogs:\n";
    for dog in chat_dogs[update.message.chat.id]:
        msg += " <a href=\"tg://user?id=" + str(dog[0].id) + "\">" + dog[0].first_name + "</a>: " + str(dog[2]) + "/" + str(dog[1]) + "\n"
    update.message.reply_text(msg, parse_mode="HTML")
updater = Updater("1728808735:AAES7qeCIRcQ2GpzfzXvEkzISaam5rO17CY", use_context=True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("end", end))
dp.add_handler(CommandHandler("stats", stats))
dp.add_handler(MessageHandler(Filters.all & ~Filters.command, count))

updater.start_polling()

updater.idle()
