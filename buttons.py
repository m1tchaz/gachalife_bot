from telebot import types
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.asyncio_filters import AdvancedCustomFilter


class CallbackFilter(AdvancedCustomFilter):
    key = 'config'

    async def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
clear_markup = types.ReplyKeyboardRemove(selective=False)


statsbtn = types.KeyboardButton('character 🫀')
nonebtn = types.KeyboardButton('village ❗')
gachabtn = types.KeyboardButton('wishing 🛐')
inventorybtn = types.KeyboardButton('inventory 💼')
raidbtn = types.KeyboardButton('pve ⚔')
dailybtn = types.KeyboardButton('commissions ⚛')
main_markup.add(statsbtn, nonebtn, gachabtn, inventorybtn, raidbtn, dailybtn)

additional_callback = CallbackData('btn_name', prefix='added')
main_stat_btn = types.InlineKeyboardButton(text='🦋traveler', callback_data=additional_callback.new(btn_name='main'))
stat_back_btn = types.InlineKeyboardButton(text='back🚪', callback_data=additional_callback.new(btn_name='back'))
curr_btn = types.InlineKeyboardButton(text='💸currency', callback_data=additional_callback.new(btn_name='currency'))
rewards_btn = types.InlineKeyboardButton(text='rewards🏆', callback_data=additional_callback.new(btn_name='rewards'))
settings_btn = types.InlineKeyboardButton(text='📊statistics',
                                          callback_data=additional_callback.new(btn_name='setting'))
talents_btn = types.InlineKeyboardButton(text='talents🌼', callback_data=additional_callback.new(btn_name='talents'))
additional_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        main_stat_btn, rewards_btn,
    ],
    [
        settings_btn, talents_btn
    ],
    [
        curr_btn, stat_back_btn
    ]
])

questing_callback = CallbackData('btn_name', prefix='quest')
addquestbtn = types.InlineKeyboardButton(text='✏Add quest', callback_data=questing_callback.new(btn_name='add'))
completeqstnbtn = types.InlineKeyboardButton(text='🔍Check quest',
                                             callback_data=questing_callback.new(btn_name='check'))
backbtn = types.InlineKeyboardButton(text='🚪Back', callback_data=questing_callback.new(btn_name='back'))
questing_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        addquestbtn, completeqstnbtn, backbtn
    ],
])

quest_conf_callback = CallbackData('btn_name', prefix='quest_conf')
yessmilebtn = types.InlineKeyboardButton(text='yep', callback_data=quest_conf_callback.new(btn_name='yes'))
changequestbtn = types.InlineKeyboardButton(text='change Something',
                                            callback_data=quest_conf_callback.new(btn_name='change'))
quest_conf_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        yessmilebtn, changequestbtn
    ]
])

yes_or_no_callback = CallbackData('btn_name', prefix='quest_splitting')
yesinlinebtn = types.InlineKeyboardButton(text='yep', callback_data=yes_or_no_callback.new(btn_name='yes'))
nobtn = types.InlineKeyboardButton(text='nope', callback_data=yes_or_no_callback.new(btn_name='no'))
yes_no_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        yesinlinebtn, nobtn
    ]
])

yesbtn = types.KeyboardButton('yep')
nobtn = types.KeyboardButton('no')
yes_or_no_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(yesbtn, nobtn)

back_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(backbtn)
back_inline_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        backbtn
    ]
])


dif_callback = CallbackData('dif_name', prefix='diff')
btn = []
for i in range(1, 6):
    btn.append(types.InlineKeyboardButton(text=f'{i}', callback_data=dif_callback.new(dif_name=str(i))))
dif_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        btn[0], btn[1], btn[2], btn[3], btn[4],
    ]
])


types_callback = CallbackData('type_name', prefix='type')
physics_btn = types.InlineKeyboardButton(text='physics', callback_data=types_callback.new(type_name='physics'))
wisdom_btn = types.InlineKeyboardButton(text='wisdom', callback_data=types_callback.new(type_name='wisdom'))
intelligence_btn = types.InlineKeyboardButton(text='intelligence',
                                              callback_data=types_callback.new(type_name='intelligence'))
health_btn = types.InlineKeyboardButton(text='health', callback_data=types_callback.new(type_name='health'))
types_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        physics_btn, wisdom_btn, intelligence_btn, health_btn
    ]
])

factor_callback = CallbackData('factor', prefix='factor')
factor_yes_btn = types.InlineKeyboardButton(text='yep', callback_data=factor_callback.new(factor='yes'))
factor_no_btn = types.InlineKeyboardButton(text='nope', callback_data=factor_callback.new(factor='no'))
factor_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        factor_yes_btn, factor_no_btn
    ]
])

wish_callback = CallbackData('banner_name', prefix='wish')
primo_banner_btn = types.InlineKeyboardButton(text='secretum secretorum',
                                              callback_data=wish_callback.new(banner_name='primogems'))
dust_banner_btn = types.InlineKeyboardButton(text='epitome invocation',
                                             callback_data=wish_callback.new(banner_name='dust'))
mora_banner_btn = types.InlineKeyboardButton(text='MoraBanner',
                                             callback_data=wish_callback.new(banner_name='mora'))
wish_back_btn = types.InlineKeyboardButton(text='back', callback_data=wish_callback.new(banner_name='back'))
wish_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        primo_banner_btn, dust_banner_btn
    ],
    [
        wish_back_btn
    ]
])

primo_banner_callback = CallbackData('banner_roll', prefix='banner1')
roll_banner_btn = types.InlineKeyboardButton(text='roll', callback_data=primo_banner_callback.new(banner_roll='roll'))
back_banner_btn = types.InlineKeyboardButton(text='back', callback_data=primo_banner_callback.new(banner_roll='back'))
primo_banner_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        roll_banner_btn, back_banner_btn
    ]
])

storage_callback = CallbackData('storage_name', prefix='storage')
life_inventory_btn = types.InlineKeyboardButton(text='Life Storage',
                                                callback_data=storage_callback.new(storage_name='life'))
game_inventory_btn = types.InlineKeyboardButton(text='Game Storage',
                                                callback_data=storage_callback.new(storage_name='game'))
storage_back_btn = types.InlineKeyboardButton(text='Back',
                                              callback_data=storage_callback.new(storage_name='back'))
storage_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        life_inventory_btn, game_inventory_btn
    ],
    [
        storage_back_btn
    ]

])

life_inventory_callback = CallbackData('rarity', prefix='life_item_rarity')
rare_inventory_btn = types.InlineKeyboardButton(text='3 ⭐', callback_data=life_inventory_callback.new(rarity='rare'))
epic_inventory_btn = types.InlineKeyboardButton(text='4 ⭐', callback_data=life_inventory_callback.new(rarity='epic'))
legendary_inventory_btn = types.InlineKeyboardButton(text='5 ⭐',
                                                     callback_data=life_inventory_callback.new(rarity='legendary'))
life_inventory_back_btn = types.InlineKeyboardButton(text='back',
                                                     callback_data=life_inventory_callback.new(rarity='back'))
life_inventory_use_btn = types.InlineKeyboardButton(text='use', callback_data=life_inventory_callback.new(rarity='use'))
life_inventory_rare_epic_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        rare_inventory_btn, epic_inventory_btn
    ],
    [
        life_inventory_use_btn
    ],
    [
        life_inventory_back_btn
    ]
])
life_inventory_legendary_epic_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        legendary_inventory_btn, epic_inventory_btn
    ],
    [
        life_inventory_use_btn
    ],
    [
        life_inventory_back_btn
    ]
])
life_inventory_rare_legendary_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        rare_inventory_btn, legendary_inventory_btn
    ],
    [
        life_inventory_use_btn
    ],
    [
        life_inventory_back_btn
    ]
])

life_inventory_use_callback = CallbackData('rarity', prefix='life_use')
rare_use_inventory_btn = types.InlineKeyboardButton(text='3 ⭐',
                                                    callback_data=life_inventory_use_callback.new(rarity='rare'))
epic_use_inventory_btn = types.InlineKeyboardButton(text='4 ⭐',
                                                    callback_data=life_inventory_use_callback.new(rarity='epic'))
legendary_use_inventory_btn = types.InlineKeyboardButton(text='5 ⭐',
                                                         callback_data=life_inventory_use_callback.new(
                                                             rarity='legendary'))
life_use_inventory_back_btn = types.InlineKeyboardButton(text='back',
                                                         callback_data=life_inventory_use_callback.new(rarity='back'))
life_inventory_use_markup = types.InlineKeyboardMarkup(keyboard=[
    [
        rare_use_inventory_btn, epic_use_inventory_btn, legendary_use_inventory_btn
    ],
    [
        life_use_inventory_back_btn
    ]
])

areas_btn = types.KeyboardButton('search areas')
dungeons_btn = types.KeyboardButton('dungeons')
pve_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(areas_btn, dungeons_btn)

check_deilies_btn = types.KeyboardButton('check dailies')
daily_add_btn = types.KeyboardButton('add dailies')
delete_deilies_btn = types.KeyboardButton('delete dailies')
daily_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(check_deilies_btn, daily_add_btn,
                                                                                delete_deilies_btn, backbtn)

attack_btn = types.KeyboardButton('attack')
retreat_btn = types.KeyboardButton('retreat')
find_another_btn = types.KeyboardButton('find another')
fight_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)\
    .add(attack_btn, find_another_btn, retreat_btn)

