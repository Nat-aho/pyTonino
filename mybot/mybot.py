import telegram
import logging


def get_starting_message(bot_name):
    msg = f"Ciao! Sono {bot_name}! Ti aiuterò a sapere quando" +\
            "pubblicheranno un nuovo file."
    return msg


def get_good_news_message(new_file_path):
    msg = f"Hanno messo un nuovo file!\n{new_file_path}"
    return msg


async def send(msg, chat_id, token):
    """
    Send a message "msg" to a telegram user or group specified by "chat_id"
    """
    bot = telegram.Bot(token=token)
    await bot.sendMessage(chat_id=chat_id, text=msg)
    logging.info('Message Sent!')
