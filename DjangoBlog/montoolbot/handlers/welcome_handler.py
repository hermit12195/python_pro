from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from database.db import user_list
from handlers.profile_handler import profile
from utils.states import HANDLE_OPTION, ASK_NAME


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
   keyboard = [
      [InlineKeyboardButton("My Profile", callback_data="profile")],
      [InlineKeyboardButton("About Us", callback_data="about")]
   ]
   markup = InlineKeyboardMarkup(keyboard)
   await update.message.reply_text("Took you back to the Welcome Menu", reply_markup=ReplyKeyboardRemove())
   await update.message.reply_text("Choose option:", reply_markup=markup)
   return HANDLE_OPTION


async def handle_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
   query = update.callback_query
   option = query.data
   print("handle option is triggered")
   if option == "about":
      await context.bot.send_message(chat_id=query.message.chat.id, text="We are professionals!")
   elif option == "profile":
      user_id=update.effective_user.id
      context.user_data["user_id"]= user_id
      user = await user_list(user_id)
      if user is not None:
         await context.bot.send_message(chat_id=query.message.chat.id, text = f"Hope you are fine today, {user[1]}!")
         context.user_data["user_id"] = user[0]
         context.user_data["user_name"] = user[1]
         context.user_data["user_phone"] = user[2]
         return await profile(update, context)
      else:
         await context.bot.send_message(chat_id=query.message.chat.id, text =f"Well, you don`t have profile yet:(\n But don`t worry, we`ll handle it in a moment.\n Please provide your name:")
         return ASK_NAME