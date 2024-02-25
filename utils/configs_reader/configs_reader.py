import yaml
import logging

def read_telegram_configs(file, bot, chat):
    """
    Read telegram configurations from a yaml file
    """
    logging.info(f"Reading telegram configs from {file}")
    with open(file, 'r') as f:
        configs = yaml.safe_load(f)
    
    bot_congifs  = configs["bot"][bot]
    chat_congifs = configs["chat"][chat]

    return {"bot": bot_congifs, "chat": chat_congifs}

