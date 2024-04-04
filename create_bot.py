from aiogram import Bot, Dispatcher
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher()
