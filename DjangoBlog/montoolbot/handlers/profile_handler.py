import uuid

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from handlers.back_handler import back
from utils.states import HANDLE_OPTION2, ADMIN_REDIRECT, BACK


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("profile is triggered")
    await context.bot.send_message(chat_id=context.user_data["user_id"], text=
    f"Profile loaded!\n"
    f"Name: {context.user_data['user_name']}\n"
    f"Phone: {context.user_data['user_phone']}"
                                   )
    keyboard = [["My Servers", "My Balance"], ["Support", "Back to Welcome Menu"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await context.bot.send_message(
        chat_id=context.user_data["user_id"],
        text="Choose option:",
        reply_markup=markup
    )
    return HANDLE_OPTION2


async def handle_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    option = update.message.text
    if option == "My Servers":
        await context.bot.send_message(chat_id=context.user_data["user_id"], text="Here is the list of your servers:")
    elif option == "Support":
        context.user_data["case_id"] = uuid.uuid4().hex[:8]
        await update.message.reply_text("Please explain in detail the matter of your request:")
        return ADMIN_REDIRECT
    elif option == "My Balance":
        await context.bot.send_message(chat_id=context.user_data["user_id"],
                                       text="Common, man! You are homeless, you have zero balance:)")
    elif option == "Back to Welcome Menu":
        return await back(update, context)
