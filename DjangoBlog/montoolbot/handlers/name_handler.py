from telegram import Update
from telegram.ext import ContextTypes

from handlers.phone_handler import collect_phone
from utils.states import ASK_PHONE


async def collect_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text
    context.user_data["user_name"] = user_name
    print("tut0")
    return await collect_phone(update, context)