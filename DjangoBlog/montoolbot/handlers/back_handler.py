from telegram import Update
from telegram.ext import ContextTypes



async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
   print("back state is triggered")
   from handlers.welcome_handler import welcome
   return await welcome(update, context)