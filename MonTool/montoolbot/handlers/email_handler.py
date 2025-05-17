from telegram import Update
from telegram.ext import ContextTypes




async def collect_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from handlers.phone_handler import collect_phone
    user_email = update.message.text
    context.user_data["user_email"] = user_email
    return await collect_phone(update, context)