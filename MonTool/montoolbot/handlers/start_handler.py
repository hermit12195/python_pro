from telegram import Update
from telegram.ext import ContextTypes


from handlers.welcome_handler import welcome



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
   context.user_data.clear()
   context.chat_data.clear()
   await update.message.reply_text("Hello! Welcome to Mon-Tool. \nWe are specialized in a comprehensive production workloads monitoring with advanced tooling.")
   return await welcome(update, context)





