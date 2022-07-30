import asyncio
import random
from datetime import datetime
import pytz
from config import db_object, db_connection
import math

lvl_dict = {
    1: 0, 2: 525, 3: 1235, 4: 2021, 5: 3403, 6: 7138, 7: 10053, 8: 13804, 9: 18512, 10: 24297,
    11: 85990, 12: 117506, 13: 157384, 14: 207736, 15: 269997, 16: 346462, 17: 439268, 18: 551295, 19: 685171,
    20: 843709, 21: 1030734, 22: 1249629, 23: 1504995, 24: 1800847, 25: 2142652, 26: 2535122, 27: 2984677,
    28: 3496798, 29: 4080655, 30: 472836, 31: 6025, 32: 6300, 33: 6600, 34: 6900, 35: 7175, 36: 7475, 37: 7750,
    38: 8050, 39: 8325, 40: 8625, 41: 10550, 42: 11525, 43: 12475, 44: 13450, 45: 14400, 46: 15350, 47: 16325,
    48: 17275, 49: 18250, 50: 9999999
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
        'genshin1hour', 'manga30min', 'manga1hour', 'show1', 'show2',
    ],
    4: [
        'genshin2hour', 'genshin3hour', 'genshin4hour', 'manga2hour', 'show3', 'show4', 'show5'
    ],
    5: [
        'genshin5hour', 'manga4hour', 'movie', 'show6'
    ]
}


def wish_processing(wish_type):

    if wish_type == 'primogems':
        wished_number = random.randint(1, 10000)
        print(wished_number)
        if wished_number < 3333:
            return 5
        elif wished_number < 6666:
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


first_area_dict = {
    'slime': [1, 25, 4, 6],
    'wolf': [2, 50, 5, 8],
    'azir': [3, 75, 4, 6],
    'ezreal': [4, 100, 5, 8],
    'bold guy': [5, 120, 5, 8]
}
