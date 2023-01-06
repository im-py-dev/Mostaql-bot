import json
import logging
import os
import sys
import telebot
from dotenv import load_dotenv
from threading import Lock


def read_json(file_path: str):
    with open(f"{file_path}", encoding='utf-8') as f:
        return json.load(f)


def get_json(class_name, file_name):
    return class_name(read_json(f"{JSON_PATH}/{file_name}"))


def get_server_state():
    return read_json(f"{JSON_PATH}/server_state.json")['STATE']


lock = Lock()
logger = telebot.logger
logger.setLevel(logging.WARNING)

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
ADMIN_PATH = os.path.join(PROJECT_PATH, 'Admin')
JSON_PATH = os.path.join(PROJECT_PATH, 'Json')

try:
    load_dotenv()
    API_KEY = os.getenv('TELEGRAM_BOT_API_KEY')
    DEVELOPER_ID = int(os.getenv('DEVELOPER_ID'))
    ADMIN_ID = int(os.getenv('ADMIN_ID'))
except (TypeError, ValueError) as r:
    sys.exit()

ADMINS_UID = [
    ADMIN_ID,
]
