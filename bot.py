"""
Lucas Analyse ⚽️ Bot — Text Utility Bot
Works entirely inside Telegram using a persistent reply keyboard.
Every message includes a "Click to Join" button linking to the channel.
No AI API — pure text logic only.
"""
import logging
import os

from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import text_tools

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_LINK = "https://t.me/+aZyjCO1v0yoxNWQ1"

# Conversation states
CHOOSING, TYPING_SORT, TYPING_DEDUPE = range(3)

# Button labels — must match exactly between keyboard and handlers
BTN_SORT = "🔤 Sort Text Lists"
BTN_DEDUPE = "🗑️ Remove Duplicate Lines"
BTN_GUIDE = "📖 Quick Guide"
BTN_HELP = "⚙️ Help / Info"

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [[BTN_SORT, BTN_DEDUPE], [BTN_GUIDE, BTN_HELP]],
    resize_keyboard=True,
)

JOIN_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("✅ Click to Join", url=CHANNEL_LINK)]]
)

WELCOME_TEXT = (
    "👋 Welcome to Lucas analyse ⚽️!\n\n"
    "I'm here to make your everyday text tasks faster. I offer two simple, "
    "reliable tools:\n"
    "• 🔤 Sort Text Lists – alphabetically sort lines A-Z\n"
    "• 🗑️ Remove Duplicate Lines – keep only unique lines\n\n"
    "📖 Quick Guide:\n"
    "1️⃣ Tap one of the buttons below.\n"
    "2️⃣ Paste or type your text when prompted.\n"
    "3️⃣ Receive the cleaned result instantly.\n\n"
    "Use the buttons anytime to start a new task or get help."
)

QUICK_GUIDE_TEXT = (
    "📖 Quick Guide:\n\n"
    "1️⃣ Tap 'Sort Text Lists' or 'Remove Duplicate Lines'\n"
    "2️⃣ Paste or type your list — one item per line\n"
    "3️⃣ I'll instantly send back the cleaned result\n\n"
    "You can start a new task anytime using the buttons below."
)

HELP_TEXT = (
    "⚙️ Help / Info\n\n"
    "Lucas analyse ⚽️ provides quick text tools for everyday use — "
    "entirely inside Telegram, no external site needed.\n\n"
    "Available tools:\n"
    "• Sort Text Lists — alphabetically sorts your lines A-Z\n"
    "• Remove Duplicate Lines — keeps only unique lines, in original order\n\n"
    "Type /start anytime to return to the main menu."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=MAIN_KEYBOARD)
    await update.message.reply_text("Stay updated:", reply_markup=JOIN_BUTTON)
    return CHOOSING


async def sort_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Paste or type your list below — one item per line — "
        "and I'll sort it alphabetically A-Z.",
        reply_markup=JOIN_BUTTON,
    )
    return TYPING_SORT


async def dedupe_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Paste or type your list below — one item per line — "
        "and I'll remove any duplicate lines.",
        reply_markup=JOIN_BUTTON,
    )
    return TYPING_DEDUPE


async def do_sort(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    result = text_tools.sort_lines(text)
    await update.message.reply_text(f"✅ Sorted result:\n\n{result}", reply_markup=MAIN_KEYBOARD)
    await update.message.reply_text("Stay updated:", reply_markup=JOIN_BUTTON)
    return CHOOSING


async def do_dedupe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    result = text_tools.remove_duplicates(text)
    await update.message.reply_text(f"✅ Cleaned result:\n\n{result}", reply_markup=MAIN_KEYBOARD)
    await update.message.reply_text("Stay updated:", reply_markup=JOIN_BUTTON)
    return CHOOSING


async def quick_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(QUICK_GUIDE_TEXT, reply_markup=MAIN_KEYBOARD)
    await update.message.reply_text("Stay updated:", reply_markup=JOIN_BUTTON)
    return CHOOSING


async def help_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, reply_markup=MAIN_KEYBOARD)
    await update.message.reply_text("Stay updated:", reply_markup=JOIN_BUTTON)
    return CHOOSING


async def fallback_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please use one of the buttons below to get started.",
        reply_markup=MAIN_KEYBOARD,
    )
    await update.message.reply_text("Stay updated:", reply_markup=JOIN_BUTTON)
    return CHOOSING


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Cancelled. Tap a button below to start again.", reply_markup=MAIN_KEYBOARD
    )
    return CHOOSING


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set.")

    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(filters.Regex(f"^{BTN_SORT}$"), sort_prompt),
                MessageHandler(filters.Regex(f"^{BTN_DEDUPE}$"), dedupe_prompt),
                MessageHandler(filters.Regex(f"^{BTN_GUIDE}$"), quick_guide),
                MessageHandler(filters.Regex(f"^{BTN_HELP}$"), help_info),
                MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_message),
            ],
            TYPING_SORT: [
                MessageHandler(filters.Regex(f"^{BTN_SORT}$"), sort_prompt),
                MessageHandler(filters.Regex(f"^{BTN_DEDUPE}$"), dedupe_prompt),
                MessageHandler(filters.Regex(f"^{BTN_GUIDE}$"), quick_guide),
                MessageHandler(filters.Regex(f"^{BTN_HELP}$"), help_info),
                MessageHandler(filters.TEXT & ~filters.COMMAND, do_sort),
            ],
            TYPING_DEDUPE: [
                MessageHandler(filters.Regex(f"^{BTN_SORT}$"), sort_prompt),
                MessageHandler(filters.Regex(f"^{BTN_DEDUPE}$"), dedupe_prompt),
                MessageHandler(filters.Regex(f"^{BTN_GUIDE}$"), quick_guide),
                MessageHandler(filters.Regex(f"^{BTN_HELP}$"), help_info),
                MessageHandler(filters.TEXT & ~filters.COMMAND, do_dedupe),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
    )

    app.add_handler(conv_handler)

    logger.info("Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
