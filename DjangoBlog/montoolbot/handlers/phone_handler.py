from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from database.db import create_user
from handlers.profile_handler import profile
from utils.states import PROFILE, WAITING_FOR_CONTACT


async def collect_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("tut1")
    phone_button = KeyboardButton("📱 Share Phone Number", request_contact=True)
    keyboard = [[phone_button]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        f"Got your name, {context.user_data["user_name"]}! Now, please provide your phone number:", reply_markup=markup)
    return WAITING_FOR_CONTACT


async def create(update, context):
    if update.message.contact is not None:
        context.user_data["user_phone"] = update.message.contact["phone_number"]
        await create_user(context.user_data["user_id"], context.user_data["user_name"], context.user_data["user_phone"])
        print("tut3")
    return await profile(update, context)