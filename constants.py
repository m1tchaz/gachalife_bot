import random

rank_dict = {
    1: 0, 2: 375, 3: 500, 4: 625, 5: 725, 6: 850, 7: 950, 8: 1075, 9: 1200, 10: 1300,
    11: 1425, 12: 1525, 13: 1650, 14: 1775, 15: 1875, 16: 2000, 17: 2375, 18: 2500, 19: 2625, 20: 2775,
    21: 2825, 22: 3425, 23: 3725, 24: 4000, 25: 4300, 26: 4575, 27: 4875, 28: 5150, 29: 5450,
    30: 5725, 31: 6025, 32: 6300, 33: 6600, 34: 6900, 35: 7175, 36: 7475, 37: 7750, 38: 8050, 39: 8325, 40: 8625,
    41: 10550, 42: 11525, 43: 12475, 44: 13450, 45: 14400, 46: 15350, 47: 16325, 48: 17275, 49: 18250, 50: 9999999
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
