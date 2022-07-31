import random
from states import *
from buttons import *
from config import *
from telebot import types
import asyncio
from constants import first_area_dict, lvl_dict, areas_dict


class Enemy:
    def __init__(self, name, place):
        self.name = name
        self.place = place
        self.lvl = place[self.name][0]
        self.health = place[self.name][1]
        self.min_attack = place[self.name][2]
        self.max_attack = place[self.name][3]
        self.photo = place[self.name][4]


class Hero:
    def __init__(self, ids):
        slt = 'SELECT max_health,physics,wisdom,intelligence from stats WHERE id =%s'
        db_object.execute(slt, (ids,))
        result = db_object.fetchall()
        lvl_slt = 'SELECT lvl FROM users where id=%s'
        db_object.execute(lvl_slt, (ids, ))
        self.lvl = db_object.fetchone()[0]
        self.health = result[0][0]
        self.physics = result[0][1]
        self.wisdom = result[0][2]
        self.intelligence = result[0][3]
        self.min_attack = 4 * self.lvl
        self.max_attack = 6 * self.lvl


async def fight(hero, opponent, message):
    while hero.health > 0 and opponent.health > 0:
        await asyncio.sleep(1)
        enemy_dmg = random.randint(opponent.min_attack, opponent.max_attack)
        hero_dmg = random.randint(hero.min_attack, hero.max_attack)
        opponent.health = opponent.health - hero_dmg
        hero.health = hero.health - enemy_dmg
        if opponent.health < 0:
            opponent.health = 0
        if hero.health < 0:
            hero.health = 0
        await bot.edit_message_text(text=f'you have done {hero_dmg} dmg\n'
                                         f'while you opponent did {enemy_dmg}\n\n'
                                         f'your health:{hero.health}\nenemy health:{opponent.health}',
                                    chat_id=message.chat.id, message_id=message.message_id)
    if hero.health <= 0:
        return False
    else:
        return True


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
        area_btn = types.KeyboardButton(f'{areas_dict[area]}')
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
    if message.text == 'desert':
        global enemy, msg
        enemy = random.choice(list(first_area_mobs.values()))
        photo = open(enemy.photo, 'rb')
        await bot.send_photo(message.chat.id, photo)
        msg = await bot.send_message(message.chat.id, f'you have encountered <b>{enemy.name}</b> '
                                                      f'with lvl of <b>{enemy.lvl}</b>',
                                     parse_mode='HTML', reply_markup=fight_markup)
        await bot.set_state(message.chat.id, States.pve_area_farm, message.chat.id)
    elif message.text == 'test1':
        await bot.set_state(message.chat.id, States.main, chat_id=message.chat.id)
        await bot.send_message(message.chat.id, 'nothing is here yet', reply_markup=main_markup)
    else:
        await bot.set_state(message.chat.id, States.main, chat_id=message.chat.id)
        await bot.send_message(message.chat.id, 'go fuck anywhere else/back button', reply_markup=main_markup)


@bot.message_handler(state=States.pve_area_farm)
async def area_farming(message):
    global enemy, msg
    if message.text == 'attack':
        energy_select = 'SELECT energy FROM users where id =%s'
        db_object.execute(energy_select, (message.chat.id, ))
        if db_object.fetchone()[0] >= 10:
            if 'enemy' in globals():
                hero = Hero(message.chat.id)
                msg = await bot.send_message(message.chat.id, 'initiating the fight in 1 second', reply_markup=None)
                await asyncio.sleep(1)
                result_of_fight = await fight(hero, enemy, msg)
                if result_of_fight:
                    lvl_slt = 'SELECT lvl FROM users WHERE id= %s'
                    db_object.execute(lvl_slt, (message.chat.id,))
                    lvl = db_object.fetchone()[0]
                    start_lvl_select = 'SELECT start_lvl from USERS WHERE id=%s'
                    db_object.execute(start_lvl_select, (message.chat.id,))
                    start_lvl = db_object.fetchone()[0]
                    if start_lvl == 0:
                        start_lvl = lvl
                        start_lvl_update = 'UPDATE users SET start_lvl = %s WHERE id = %s'
                        db_object.execute(start_lvl_update, (start_lvl, message.chat.id))
                    full_exp_day = 0
                    for lvl_number in range(start_lvl + 1, start_lvl + 4):
                        full_exp_day += lvl_dict[lvl_number]
                    exp_reward = full_exp_day * 0.025
                    upd = 'UPDATE users SET exp = exp + %s WHERE id = %s RETURNING exp'
                    db_object.execute(upd, (exp_reward, message.chat.id))
                    new_exp = db_object.fetchall()[0][0]
                    if new_exp > 15 and lvl == start_lvl + 3:
                        upd = 'UPDATE users SET exp = exp - %s WHERE id = %s'
                        db_object.execute(upd, (exp_reward, message.chat.id))
                        exp_reward = 0
                    while new_exp >= lvl_dict[lvl + 1]:
                        upd_lvl = 'UPDATE users SET lvl = lvl + 1 WHERE id= %s'
                        db_object.execute(upd_lvl, (message.chat.id,))
                        new_exp = new_exp - lvl_dict[lvl + 1]
                        upd_exp = 'UPDATE users set exp = %s WHERE id = %s'
                        db_object.execute(upd_exp, (new_exp, message.chat.id))
                        lvl = lvl + 1
                    energy_update = 'UPDATE users SET energy = energy - 10 WHERE id =%s'
                    db_object.execute(energy_update, (message.chat.id,))
                    db_connection.commit()
                    await bot.edit_message_text(text='you won the fight\n\n'
                                                     f'xp gotten {exp_reward}\n\n'
                                                     f'energy used 10', chat_id=message.chat.id,
                                                message_id=msg.message_id)
                else:
                    await bot.edit_message_text(text='you have died', chat_id=message.chat.id, message_id=msg.message_id)
                del enemy
            else:
                await bot.send_message(message.chat.id, 'you should find an enemy', reply_markup=fight_markup)
        else:
            await bot.send_message(message.chat.id, 'not enough energy', reply_markup=fight_markup)
    elif message.text == 'find another':
        enemy = random.choice(list(first_area_mobs.values()))
        photo = open(enemy.photo, 'rb')
        await bot.send_photo(message.chat.id, photo)
        await bot.send_message(message.chat.id, f'you have encountered <b>{enemy.name}</b> '
                                                f'with lvl of <b>{enemy.lvl}</b>',
                               parse_mode='HTML', reply_markup=fight_markup)
    elif message.text == 'retreat':
        markup = await available_areas(message.chat.id)
        await bot.send_message(message.chat.id, 'retreating', reply_markup=markup)
        await bot.set_state(message.chat.id, States.pve_area_choose)
