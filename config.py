import psycopg2
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from datetime import datetime
import pytz


def get_time():
    samara_time = pytz.timezone('Europe/Samara')
    time = datetime.now(samara_time)
    return time.strftime("%H:%M:%S")[:2]


API_KEY = '5360806461:AAHtoCHkJu17oCp9vmLIeRrfO4u9cQtiPio'
DB_URI = 'postgres://mfqieqdxflknqf:789cf483df8013c1caf305e1dbd345923ebb795c818e2eed8de80be3fe' \
         'e8b900@ec2-52-54-212-232.compute-1.amazonaws.com:5432/d6bgik450kutrb'

bot = AsyncTeleBot(API_KEY, state_storage=StateMemoryStorage())

db_connection = psycopg2.connect(DB_URI, sslmode='require')
db_object = db_connection.cursor()
