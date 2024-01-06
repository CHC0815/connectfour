import logging
import os
import pickle
import sqlite3
from io import BytesIO

from PIL import Image, ImageDraw
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PicklePersistence,
    filters,
)

from agents.random_bot import bot as RandomBot
from connectfour.ConnectFour import ConnectFour
from connectfour.ConnectFourConfig import ConnectFourConfig
from connectfour.Observation import Observation

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

db: sqlite3.Connection = sqlite3.connect("connectfourbot.db")


def user_move(obs: Observation, config: ConnectFourConfig) -> int:
    return 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        return
    safe_game(
        update.effective_chat.id,
        ConnectFour(
            user_move,
            RandomBot,
        ),
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Let's play Connect Four!"
    )


def dummy_photo(n: int | str = ""):
    img = Image.new(mode="RGB", size=(400, 400))
    draw = ImageDraw.Draw(img)
    draw.rectangle((20, 20, 380, 380), fill="white")
    draw.text((10, 10), f"{n}")

    bio = BytesIO()
    img.save(bio, "PNG")
    bio.seek(0)
    return bio


def get_game(chat_id: int) -> ConnectFour:
    board = (
        db.cursor().execute("SELECT board FROM games WHERE chat_id = ?", (chat_id,)).fetchall()[0]
    )
    return pickle.loads(board)


def safe_game(chat_id: int, game: ConnectFour):
    db.cursor().execute("REMOVE FROM games WHERE chat_id = ?", (chat_id,))
    db.cursor().execute("INSERT INTO games VALUES (?, ?)", (chat_id, str(pickle.dumps(game))))


async def board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        return

    db.cursor().execute("REMOVE FROM games WHERE chat_id = ?", (update.effective_chat.id,))
    db.cursor().execute("INSERT INTO games VALUES (?, ?)", (update.effective_chat.id, "0"))

    keyboard = [
        [InlineKeyboardButton("⬆", callback_data=f"{i}") for i in range(7)],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=dummy_photo(),
        reply_markup=reply_markup,
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is None:
        return
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("⬆", callback_data=f"{i}") for i in range(7)],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_media(
        media=InputMediaPhoto(
            media=dummy_photo(query.data or ""),
        ),
        reply_markup=reply_markup,
    )


if __name__ == "__main__":
    db.cursor().execute(open("setup.sql").read())

    application = ApplicationBuilder().token(os.environ.get("BOT_TOKEN") or "").build()

    start_handler = CommandHandler("start", start)
    board_handler = CommandHandler("new_game", board)
    application.add_handler(start_handler)
    application.add_handler(board_handler)
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()
