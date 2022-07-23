import random
from states import *
from buttons import *
from config import *
from telebot import types
from constants import first_area_dict
import asyncio


class Enemy:
    def __init__(self, name, place):
        self.name = name
        self.place = place
        self.lvl = place[self.name][0]
        self.health = place[self.name][1]
        self.min_attack = place[self.name][2]
        self.max_attack = place[self.name][3]


global enemy


async def available_areas(ids):
    slt = "SELECT lvl FROM users WHERE id = %s"
    db_object.execute(slt, (ids, ))
    lvl = db_object.fetchone()[0]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for area in range(1, lvl//10 + 2):
        area_btn = types.KeyboardButton(f'1-{area*10} area')
        markup.add(area_btn)
    return markup


@bot.message_handler(state=States.pve_main)
async def change_target_location(message):
    if message.text == 'search areas':
        markup = await available_areas(message.chat.id)
        await bot.send_message(message.chat.id, 'choose an area to go for',
                               reply_markup=markup)
        await bot.set_state(message.chat.id, States.pve_area_choose, chat_id=message.chat.id)
    elif message.text == 'dungeons':
        await bot.set_state(message.chat.id, States.main, chat_id=message.chat.id)
        await bot.send_message(message.chat.id, 'nothings is here yet/back button', reply_markup=main_markup)


@bot.message_handler(state=States.pve_area_choose)
async def area_choosing(message):
    if message.text == '1-10 area':
        global enemy, msg
        enemy = Enemy(random.choice(list(first_area_dict.keys())), first_area_dict)
        msg = await bot.send_message(message.chat.id, f'you have encountered <b>{enemy.name}</b> '
                                                f'with lvl of <b>{enemy.lvl}</b>',
                               parse_mode='HTML', reply_markup=fight_markup)
        await bot.set_state(message.chat.id, States.pve_area_farm, message.chat.id)
    else:
        await bot.set_state(message.chat.id, States.main, chat_id=message.chat.id)
        await bot.send_message(message.chat.id, 'go fuck anywhere else/back button', reply_markup=main_markup)


@bot.message_handler(state=States.pve_area_farm)
async def area_farming(message):
    global enemy, msg
    if message.text == 'attack':
        if 'enemy' in globals():
            msg = await bot.send_message(message.chat.id, 'initiating the fight in 3 second', reply_markup=None)
            await asyncio.sleep(3)
            await bot.edit_message_text(text='you have died', chat_id=message.chat.id, message_id=msg.message_id)
            del enemy
        else:
            bot.send_message(message.chat.id, 'you should find an enemy', reply_markup=fight_markup)
    elif message.text == 'find another':
        enemy = Enemy(random.choice(list(first_area_dict.keys())), first_area_dict)
        await bot.send_message(message.chat.id, f'you have encountered <b>{enemy.name}</b> '
                                                f'with lvl of <b>{enemy.lvl}</b>',
                               parse_mode='HTML', reply_markup=fight_markup)
    elif message.text == 'retreat':
        markup = await available_areas(message.chat.id)
        await bot.send_message(message.chat.id, 'retreating', reply_markup=markup)
        await bot.set_state(message.chat.id, States.pve_area_choose)