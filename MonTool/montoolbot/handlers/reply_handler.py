import os

from telegram import Update
from telegram.ext import ContextTypes


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(os.getenv("ADMIN_ID")):
        return
    client_id=update.message.text.split()[1]
    message = " ".join(update.message.text.split()[2:])
    await context.bot.send_message(chat_id=client_id, text=message)
