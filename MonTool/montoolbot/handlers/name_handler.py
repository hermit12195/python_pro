from telegram import Update
from telegram.ext import ContextTypes

from utils.states import ASK_EMAIL


async def collect_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text
    context.user_data["user_name"] = user_name
    await update.message.reply_text(f"Got your name, {context.user_data["user_name"]}! \nPlease provide your email (!Should be the same as used in MonTool service!):")
    return ASK_EMAIL