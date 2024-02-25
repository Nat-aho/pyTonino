import os
import logging
import time
import asyncio
import tenacity
from requests import ConnectionError
from mybot import mybot
from scraper import scraper
from utils.configs_reader import configs_reader as configs


# Logging settings
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
TENACITY_LOGGER = logging.getLogger("Retrying")

# Paths
CONFIGS_PATH = "configs"
DATA_PATH = "data"

# UniPD website
URL = "https://datascience.math.unipd.it/files/"
EXT = "pdf"

# Telegram configs
BOT = ""
CHAT = ""

tg_configs = configs.read_telegram_configs(
    file = os.path.join(CONFIGS_PATH, "tg.yml"),
    bot = BOT,
    chat = CHAT)

BOT_NAME  = tg_configs["bot"]["name"]
BOT_TOKEN = tg_configs["bot"]["token"]
CHAT_ID = tg_configs["chat"]["chat_id"]


# Read list of current available files
with open(os.path.join(DATA_PATH, "available_files.txt")) as f:
    files = f.read().splitlines()


# Search for new files logic
retry = tenacity.retry(
    stop=tenacity.stop_after_attempt(6),
    after=tenacity.after_log(TENACITY_LOGGER, logging.WARNING),
    retry=tenacity.retry_if_exception_type(ConnectionError),
    wait=tenacity.wait_fixed(10),
    reraise=True
)

@retry
def search_for_new_files(url, ext, token, chat_id):
    current_files = scraper.get_list_of_files(URL, EXT)
    new_files = set(current_files).difference(set(files))

    if len(new_files) > 0:
        logging.info(f"{len(new_files)} new files uploaded!")
        
        for file in new_files:
            msg = mybot.get_good_news_message(file)
            asyncio.run(
                mybot.send(msg = msg, chat_id = CHAT_ID, token = BOT_TOKEN)
            )
    else:
        logging.info("Non hanno ancora caricato niente :(")


if __name__ == "__main__":
    starttime = time.monotonic()

    starting_msg = mybot.get_starting_message(BOT_NAME)
    logging.info(starting_msg)
    
    while True:
        search_for_new_files(URL, EXT, BOT_TOKEN, CHAT_ID)
        time.sleep(60.0 - ((time.monotonic() - starttime) % 60.0))
