from telebot.asyncio_handler_backends import State, StatesGroup


class States(StatesGroup):
    register = State()
    main = State()
    inventoring = State()
    life_inventory_using = State()
    dailies_main = State()
    dailies_adding = State()
    deilies_conf = State()
    deilies_completion = State()
    deilies_delete = State()
    dailies_type = State()
    deilies_diff = State()