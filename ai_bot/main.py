import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai
import os

telegram_bot_token = 'YOU_BOT_TOKEN'
openai.api_key = 'YOU_OPEN_AI_API_KEY'


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello! I'm a W - AI chat bot. You can ask me anything and I'll do my best to answer it.")


def reply(update, context):
    user_question = update.message.text
    bot_response = get_bot_response(user_question)
    context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)


def get_bot_response(user_question):
    response = openai.Completion.create(
        prompt=f"W: {user_question}\nA:",
        temperature=1,
        engine="davinci",
        max_tokens=10,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    bot_response = response.choices[0].text.strip()
    return bot_response


if __name__ == '__main__':
    updater = Updater(token=telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    reply_handler = MessageHandler(Filters.text & ~Filters.command, reply)
    dispatcher.add_handler(reply_handler)

    updater.start_polling()
