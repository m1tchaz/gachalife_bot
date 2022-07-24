import random
from states import *
from buttons import *
from config import *
from telebot import types
import asyncio
from constants import first_area_dict


class Enemy:
    def __init__(self, name, place):
        self.name = name
        self.place = place
        self.lvl = place[self.name][0]
        self.health = place[self.name][1]
        self.min_attack = place[self.name][2]
        self.max_attack = place[self.name][3]


class Hero:
    def __init__(self, ids):
        slt = 'SELECT current_health,physics,wisdom,intelligence from stats WHERE id =%s'
        db_object.execute(slt, (ids,))
        result = db_object.fetchall()
        self.health = result[0][0]
        self.physics = result[0][1]
        self.wisdom = result[0][2]
        self.intelligence = result[0][3]
        self.min_attack = int((self.physics + self.wisdom + self.intelligence) // 3 - \
                              (self.physics + self.wisdom + self.intelligence) // 15)
        self.max_attack = int((self.physics + self.wisdom + self.intelligence) // 3 + \
                              (self.physics + self.wisdom + self.intelligence) // 15)


async def fight(hero, opponent, message):
    while hero.health > 0 and opponent.health > 0:
        await asyncio.sleep(1)
        opponent.health = opponent.health - random.randint(hero.min_attack, hero.max_attack)
        hero.health = hero.health - random.randint(opponent.min_attack, opponent.max_attack)
        await bot.edit_message_text(text=f'your health:{hero.health}\nenemy health:{opponent.health}', chat_id=message.chat.id, message_id=message.message_id)


first_area_mobs = dict()

for enemy_ in first_area_dict.keys():
    new_enemy = Enemy(enemy_, first_area_dict)
    first_area_mobs[enemy_] = new_enemy

global enemy, msg


async def available_areas(ids):
    slt = "SELECT lvl FROM users WHERE id = %s"
    db_object.execute(slt, (ids,))
    lvl = db_object.fetchone()[0]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for area in range(1, lvl // 10 + 2):
        area_btn = types.KeyboardButton(f'1-{area * 10} area')
        markup.add(area_btn)
    markup.add(backbtn)
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
        enemy = random.choice(list(first_area_mobs.values()))
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
            hero = Hero(message.chat.id)
            msg = await bot.send_message(message.chat.id, 'initiating the fight in 3 second', reply_markup=None)
            await fight(hero, enemy, msg)
            await asyncio.sleep(3)
            await bot.edit_message_text(text='you have died', chat_id=message.chat.id, message_id=msg.message_id)
            del enemy
        else:
            bot.send_message(message.chat.id, 'you should find an enemy', reply_markup=fight_markup)
    elif message.text == 'find another':
        enemy = random.choice(list(first_area_mobs.values()))
        await bot.send_message(message.chat.id, f'you have encountered <b>{enemy.name}</b> '
                                                f'with lvl of <b>{enemy.lvl}</b>',
                               parse_mode='HTML', reply_markup=fight_markup)
    elif message.text == 'retreat':
        markup = await available_areas(message.chat.id)
        await bot.send_message(message.chat.id, 'retreating', reply_markup=markup)
        await bot.set_state(message.chat.id, States.pve_area_choose)
