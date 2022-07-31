import asyncio
import random
from datetime import datetime
import pytz
from config import db_object, db_connection
import math

lvl_dict = {
    1: 525, 2: 1235, 3: 2021, 4: 3403, 5: 5002, 6: 7138, 7: 10053, 8: 13804, 9: 18512,
    10: 24297, 11: 31516, 12: 39878, 13: 50352, 14: 62261, 15: 76465, 16: 92806, 17: 112027, 18:
        133876, 19: 158538, 20: 187025, 21: 218895, 22: 255366, 23: 295852, 24: 341805, 25:
        392470, 26: 449555, 27: 512121, 28: 583857, 29: 662181, 30: 747411, 31: 844146, 32:
        949053, 33: 1064952, 34: 1192712, 35: 1333241, 36: 1487491, 37: 1656447, 38: 1841143, 39:
        2046202, 40: 2265837, 41: 2508528, 42: 2776124, 43: 3061734, 44: 3379914, 45: 3723676,
    46: 4099570, 47: 4504444, 48: 4951099, 49: 5430907, 50: 5957868, 51: 6528910, 52: 7153414, 53:
        7827968, 54: 8555414, 55: 9353933, 56: 10212541, 57: 11142646, 58: 12157041, 59: 13252160, 60:
        14441758, 61: 15731508, 62: 17127265, 63: 18635053, 64: 20271765, 65: 22044909, 66: 23950783, 67: 26019833,
    68: 28261412, 69: 30672515, 70: 33287878, 71: 36118904, 72: 39163425, 73: 42460810, 74: 46024718, 75: 49853964,
    76: 54008554, 77: 58473753, 78: 63314495, 79: 68516464, 80: 74132190, 81: 80182477, 82: 86725730, 83: 93748717,
    84: 101352108, 85: 109524907, 86: 118335069, 87: 127813148, 88: 138033822, 89: 149032822, 90: 160890604,
    91: 173648795, 92: 187372170, 93: 202153736, 94: 218041909, 95: 235163399, 96: 253547862, 97: 273358532,
    98: 294631836, 99: 317515914
}

rank_dict = {
    0: 0,
    1: 25,
    2: 5000,
    3: 10000,
    4: 20000,
    5: 30000
}

primogems_wish_outcome = {
    3: [
        'free watch of youtube for 1 hour', '1 episode of anime', '2 episode of anime/show',
        '1game/30 minutes of game time', 'discord/free 40 minutes', '2game/60 minutes of game time',
        'free watch of youtube for 30 minutes'
    ],
    4: [
        'watch a film', '4 episode of anime', '3 games / 2hour of games', 'free watch of youtube for 2 hour',
        'discord/free 90 minutes', '2 episode of show', 'small walk/ rpg development'
    ],
    5: [
        'whole day off!', '3 charges of going out\ rpg development'
    ]
}

areas_dict = {
    1: 'desert',
    2: 'test1',
    3: 'test2',
    4: 'test3'
}

first_area_dict = {
    'slime': [1, 9999, 4, 6, 'enemies/area_1/first_enemy.png']
}


def wish_processing(wish_type):
    if wish_type == 'primogems':
        wished_number = random.randint(1, 10000)
        print(wished_number)
        if wished_number < 200:
            return 5
        elif wished_number < 1300:
            return 4
        else:
            return 3
    else:
        pass


def wish_reward(wish_type, item_rarity):
    outcome = ''
    if wish_type == 'primogems':
        outcome = random.choice(primogems_wish_outcome[item_rarity])
        print(outcome)

    return outcome


def get_time():
    samara_time = pytz.timezone('Europe/Samara')
    time = datetime.now(samara_time)
    return time.strftime("%H:%M:%S")[:2]


async def dailie_reset():
    while True:
        time = get_time()
        print(time)
        if int(time) == 0:
            db_object.execute(f'UPDATE users SET start_lvl = 0')
            db_object.execute(f'UPDATE dailies SET accomplishment = 0')
            db_object.execute(f'UPDATE users set energy_left = 100')
            db_object.execute(f'UPDATE users set rank_exp_left = 1000')
            db_object.execute(f'UPDATE users set dailies_left = daily')
            db_connection.commit()
            print('daily reset was done successfully ')
        await asyncio.sleep(3600)


