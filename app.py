#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simplest Telegram Bot Demo

The bot asks a user questions rhelping maintaining everyday mindfulness and reacts to the response.

Based on `https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/timerbot.py`

Usage:
Start the bot with `python app.py`
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import random
from typing import Tuple, cast

from decouple import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Filters, InvalidCallbackData,
                          MessageHandler, Updater)

# Enable logging
logging.basicConfig(
    format="%(asctime)s : %(name)s : %(levelname)s : %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

"""
From `https://medium.com/the-ascent/10-powerful-questions-to-ask-yourself-every-day-485c68b4c9ac`
"""
questions = [
    "Who do you want to be?",
    "What are you grateful for?",
    "What will you do about the things that matter most?",
    "Which reality can you accept instead of fighting against it?",
    "How can you make someone smile?",
    "Are you a little better than yesterday?",
    "Have you protected your planet?",
    "Have you made healthier choices?",
    "Have you expressed your love for your family and friends?",
]


def build_keyboard(current_question) -> InlineKeyboardMarkup:
    """
    Helper function to build the next inline keyboard.
    An example how to use `callback_data` to encode the user choice.
    """

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Like 👍", callback_data=(1, current_question)),
                InlineKeyboardButton("Dislike 👎", callback_data=(0, current_question)),
            ]
        ]
    )


# A helper function to get a chat_id in any context
def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        # text message
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        # callback message
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        # answer in Poll
        chat_id = context.bot_data[update.poll.id]

    return chat_id


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.
# This being an example and not having context present confusing beginners,
# we decided to have it present as context.
def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    user = update.message.from_user
    chat_id = get_chat_id(update, context)
    logger.info(
        f"User [{chat_id}] started the conversation. [{user.username}] [{user.first_name} {user.last_name}]"
    )

    update.message.reply_text(
        f"Hey {user.first_name}!\nI am simple bot to help you maintain everyday mindfulness. Whenever you are up to, send me /n or /next to get a random question to contemplate for a few minutes! After each question, you can tell me if you liked it or not."
    )


# An example of a message handler
def message_callback(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = get_chat_id(update, context)
    logger.info(
        f"User [{chat_id}] sent a message: '{update.message.text}'."
    )

    update.message.reply_text(
        f"Sorry {user.first_name}, I am not yet smart enough to understand this!"
    )


def get_next_question() -> str:
    return random.choice(questions)


def format_question(question: str) -> str:
    return f"💬 {question}"


def force_next_question(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = get_chat_id(update, context)

    next_question = get_next_question()
    logger.info(f"Next question for user [{chat_id}]: {next_question}")
    update.message.reply_text(
        format_question(next_question), reply_markup=build_keyboard(next_question)
    )


# An example of a button press handler
def question_button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    score, question = cast(Tuple[int, str], query.data)

    if score == 1:
        response = "❤️"
    elif score == 0:
        response = "😢"
    else:
        response = "🤷‍♂️"

    chat_id = get_chat_id(update, context)
    logger.info(
        f"User [{chat_id}] responded to the question '{question}': {response}"
    )

    context.drop_callback_data(query)

    context.bot.send_message(chat_id=chat_id, text=response)

    next_question = get_next_question()
    context.bot.send_message(
        chat_id=chat_id,
        text=format_question(next_question),
        reply_markup=build_keyboard(next_question),
    )


def handle_invalid_question_button_callback(
    update: Update, context: CallbackContext
) -> None:
    """Informs the user that the button is no longer available."""
    update.callback_query.answer()
    update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕 Please send /n to get a new question."
    )


def main() -> None:
    """Run the bot."""

    # Create the Updater and pass it your bot's token.
    updater = Updater(
        config("TELEGRAM_BOT_KEY"),
        arbitrary_callback_data=True,
    )

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("n", force_next_question))
    dispatcher.add_handler(CommandHandler("next", force_next_question))
    dispatcher.add_handler(
        MessageHandler(filters=Filters.text, callback=message_callback)
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(
            handle_invalid_question_button_callback, pattern=InvalidCallbackData
        )
    )
    dispatcher.add_handler(CallbackQueryHandler(callback=question_button_callback))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
