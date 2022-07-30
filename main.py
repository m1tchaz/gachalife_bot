from pve import *
from constants import *
from telebot import asyncio_filters


@bot.message_handler(commands=['start'], state="*")
async def start(message):
    ids = message.chat.id
    photo = open('images/standit.jpg', 'rb')
    db_object.execute(f"SELECT id FROM users WHERE id = {ids}")
    result = db_object.fetchone()
    if not result:
        await bot.set_state(message.from_user.id, States.register, message.chat.id)
        photo = open('images/picture.jpg', 'rb')
        await bot.send_photo(message.chat.id, photo)
        await bot.send_message(message.chat.id, 'Hello Traveler! \nPick a name for your future adventure!',
                               reply_markup=clear_markup)
    else:
        await bot.set_state(message.from_user.id, States.main, message.chat.id)
        await bot.send_photo(chat_id=message.chat.id, photo=photo, reply_markup=clear_markup)
        db_object.execute(f'SELECT nickname FROM users where id ={message.chat.id}')
        name = db_object.fetchone()[0]
        await bot.send_message(message.chat.id, text=f'welcome to the journey, {name.strip()}!',
                               reply_markup=main_markup)


@bot.message_handler(state=States.register)
async def creating_a_name(message):
    name = message.text
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'All right! \nEverything is set up!', reply_markup=main_markup)

    db_object.execute("INSERT INTO users(id,nickname) VALUES(%s,%s)", (chat_id, name))
    db_connection.commit()
    db_object.execute("INSERT INTO stats(id) VALUES(%s)", (chat_id,))
    db_connection.commit()
    await bot.set_state(message.chat.id, States.main, message.chat.id)


@bot.message_handler(content_types=['text'], state=States.main)
async def main_menu(message):
    if message.text.strip() == 'character 🫀':
        photo = open('images/character_1.jpg', 'rb')
        db_object.execute(f"SELECT nickname,lvl,exp,energy,rank FROM users WHERE id = {message.chat.id}")
        res = db_object.fetchall()
        lvl = res[0][1]
        rank = res[0][4]
        if rank == 0:
            rank = 'challenger'
        else:
            rank = 'admin'
        exp_needed = lvl_dict[lvl + 1]
        db_object.execute(f'SELECT physics,wisdom,intelligence,'
                          f'current_health,max_health FROM stats WHERE id = {message.chat.id}')
        stati = db_object.fetchall()
        stats = f'👾 <b>{res[0][0].strip()}:</b>\n\n' \
                f'✨ <b>lvl:</b> <em>{lvl} ({res[0][2]}/{exp_needed})</em>\n' \
                f'🎖 <b>rank: {rank}</b>\n\n' \
                f'⚔ <b>attack:</b> <em>none</em>\n' \
                f'🛡 <b>defence:</b><em> none</em>\n\n' \
                f'❤ <b>health:</b> {stati[0][3]}/{stati[0][4]}\n' \
                f'🔋 <b>energy</b>: {res[0][3]}\n\n' \
                f'💪 <b>physics:</b><em> {format(stati[0][0], ".4f")}</em>\n' \
                f'🎩 <b>wisdom:</b><em> {format(stati[0][1], ".4f")}</em>\n' \
                f'🧠 <b>intelligence:</b><em> {format(stati[0][2], ".4f")}</em>\n'
        await bot.send_photo(message.chat.id, photo)
        await bot.send_message(message.chat.id, stats, reply_markup=additional_markup, parse_mode='HTML')

    elif message.text.strip() == 'village ❗':
        await bot.send_message(message.chat.id, 'nothing is here yet...', reply_markup=main_markup)

    elif message.text.strip() == 'wishing 🛐':
        photo = open('images\main_wish.jpg', 'rb')
        await bot.send_photo(message.chat.id, photo=photo,
                             reply_markup=wish_markup)

    elif message.text.strip() == 'inventory 💼':
        photo = open('images/inventory.jpg', 'rb')
        await bot.send_photo(photo=photo, chat_id=message.chat.id)
        await bot.send_message(message.chat.id, 'you got to the storage which box should we open?',
                               reply_markup=storage_markup)

    elif message.text.strip() == 'pve ⚔':
        await bot.set_state(message.chat.id, States.pve_main, chat_id=message.chat.id)
        await bot.send_message(message.chat.id, 'what are we doing here?', reply_markup=pve_markup)

    elif message.text.strip() == 'commissions ⚛':
        dailies = ''
        typiki = ['physics', 'wisdom', 'intelligence']
        cool_typiki = ['💪physics', '🎩wisdom', '🧠intelligence']
        count = 0
        for value in typiki:
            dailies_list = ''
            slt = f'SELECT info FROM dailies WHERE id=%s AND accomplishment=0 AND type=%s'
            db_object.execute(slt, (message.chat.id, value))
            res = db_object.fetchall()
            for number, result in enumerate(res):
                dailies_list += f'{number + 1}.' + f' {result[0]}'
            dailies += f'{cool_typiki[count]}:\n' + dailies_list + '\n'
            count += 1
        await bot.send_message(message.chat.id, f'list of uncompleted dailies \n\n{dailies}', reply_markup=daily_markup)
        await bot.set_state(message.chat.id, States.dailies_main, chat_id=message.chat.id)


@bot.message_handler(state=States.dailies_main)
async def dailies_main(message):
    if message.text.strip() == 'check dailies':
        check_deilies_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        db_object.execute(f"SELECT info FROM dailies WHERE id = {message.chat.id} AND accomplishment = 0 ")
        res = db_object.fetchall()
        if res:
            for number, value in enumerate(res):
                button = types.KeyboardButton(f'{value[0].strip()}')
                check_deilies_markup.add(button)
            await bot.send_message(message.chat.id, f'Which one have you done?\n',
                                   reply_markup=check_deilies_markup)
            await bot.set_state(message.chat.id, States.deilies_conf)
        else:
            await bot.send_message(message.chat.id, f'no dailies available or everything is done.',
                                   reply_markup=daily_markup)
    elif message.text.strip() == 'add dailies':
        await bot.send_message(message.chat.id, "What is the commission about?", reply_markup=back_markup)
        await bot.set_state(message.chat.id, States.dailies_adding, chat_id=message.chat.id)
    elif message.text.strip() == 'delete dailies':
        delete_deilies_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        db_object.execute(f"SELECT info FROM dailies WHERE id = {message.chat.id}")
        res = db_object.fetchall()
        for number, value in enumerate(res):
            button = types.KeyboardButton(f'{value[0].strip()}')
            delete_deilies_markup.add(button)
        await bot.send_message(message.chat.id, f'which one do you wanna delete?\n',
                               reply_markup=delete_deilies_markup)
        await bot.set_state(message.chat.id, States.deilies_delete)
    elif message.text.strip() == '🚪Back':
        photo = open('images/main.jpg', 'rb')
        await bot.send_photo(photo=photo, chat_id=message.chat.id, reply_markup=main_markup)
        await bot.set_state(message.chat.id, States.main, message.chat.id)


@bot.message_handler(state=States.deilies_delete)
async def daily_delete(message):
    slt = 'SELECT info FROM dailies WHERE info = %s'
    db_object.execute(slt, (message.text.strip(),))
    check = db_object.fetchone()
    if check is not None:
        dlt = 'DELETE FROM dailies WHERE info = %s'
        db_object.execute(dlt, (message.text.strip(),))
        count_upd = 'UPDATE users SET daily = daily - 1 WHERE id = %s'
        db_object.execute(count_upd, (message.chat.id,))
        count_upd = 'UPDATE users SET dailies_left = dailies_left - 1 WHERE id = %s'
        db_object.execute(count_upd, (message.chat.id,))
        db_connection.commit()
        await bot.send_message(message.chat.id, text='daily has been successfully deleted', reply_markup=daily_markup)
        await bot.set_state(chat_id=message.chat.id, state=States.dailies_main, user_id=message.chat.id)
    else:
        db_connection.commit()
        delete_deilies_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        db_object.execute(f"SELECT info FROM dailies WHERE id = {message.chat.id}")
        res = db_object.fetchall()
        for number, value in enumerate(res):
            button = types.KeyboardButton(f'{value[0].strip()}')
            delete_deilies_markup.add(button)
        await bot.send_message(message.chat.id, f'there is no daily with this name\n',
                               reply_markup=delete_deilies_markup)


@bot.message_handler(state=States.dailies_adding)
async def daily_adding(message):
    if message.text == '🚪Back':
        await bot.send_message(message.chat.id, "returned to dailies main", reply_markup=daily_markup)
        await bot.set_state(message.chat.id, States.dailies_main, message.chat.id)
    else:
        db_object.execute("INSERT INTO dailies(id,info) VALUES(%s,%s)", (1, message.text))
        db_connection.commit()
        await bot.send_message(message.chat.id, 'What is the type of the daily', reply_markup=types_markup)


@bot.callback_query_handler(func=None, config=types_callback.filter())
async def daily_type(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id, cache_time=1)
    db_object.execute(f'SELECT info from  dailies WHERE id=1')
    info = db_object.fetchone()
    db_object.execute(f'DELETE FROM dailies WHERE id=1')
    db_connection.commit()
    db_object.execute("INSERT INTO dailies(id,info,type) VALUES(%s,%s,%s)",
                      (1, info, call.data[5:].strip()))
    db_connection.commit()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='What is the difficulty of the quest', reply_markup=dif_markup)


@bot.callback_query_handler(func=None, config=dif_callback.filter())
async def daily_diff(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id, cache_time=1)
    db_object.execute(f'SELECT type from dailies WHERE id=1')
    type = db_object.fetchone()
    db_object.execute(f'SELECT info from dailies WHERE id=1')
    info = db_object.fetchone()
    db_object.execute("INSERT INTO dailies(id,info,type,difficulty) VALUES(%s,%s,%s,%s)",
                      (call.message.chat.id, info, type, call.data[5]))
    count_upd = 'UPDATE users SET daily = daily + 1 WHERE id = %s'
    db_object.execute(count_upd, (call.message.chat.id,))
    count_upd = 'UPDATE users SET dailies_left = dailies_left + 1 WHERE id = %s'
    db_object.execute(count_upd, (call.message.chat.id,))

    db_object.execute(f'DELETE FROM dailies WHERE id=1')
    db_connection.commit()

    await bot.send_message(call.message.chat.id, 'All right its added to the pole', reply_markup=daily_markup)
    await bot.set_state(call.message.chat.id, States.dailies_main, call.message.chat.id)


@bot.message_handler(state=States.deilies_conf)
async def deilies_conf(message):
    yesbutton = types.KeyboardButton('Yes')
    nobutton = types.KeyboardButton('No')
    yesno_mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yesno_mark.add(yesbutton, nobutton)
    db_object.execute(f'INSERT INTO dailies(info,id) VALUES (%s,%s)', (message.text.strip(), message.chat.id + 1))
    db_connection.commit()
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Are you sure you have completed the quest: {message.text.strip()}',
                           reply_markup=yesno_mark)
    await bot.set_state(message.chat.id, States.deilies_completion)


@bot.message_handler(state=States.deilies_completion)
async def daily_done(message):
    if message.text.strip() == 'Yes':
        msg_to_delete = await bot.send_message(text='confirming the information...', chat_id=message.chat.id,
                                               reply_markup=clear_markup)
        slt_1 = 'SELECT info FROM dailies WHERE id=%s'
        db_object.execute(slt_1, (message.chat.id + 1,))
        info_untouched = db_object.fetchone()[0]
        info = str(info_untouched).strip()
        slt = 'SELECT difficulty from dailies WHERE id= %s AND info= %s'
        db_object.execute(slt, (message.chat.id, info))
        reward = db_object.fetchone()[0]
        tp = 'SELECT type FROM dailies WHERE id = %s AND info = %s'
        db_object.execute(tp, (message.chat.id, info))
        typik = db_object.fetchone()[0]
        lvl_slt = 'SELECT lvl FROM users WHERE id= %s'
        db_object.execute(lvl_slt, (message.chat.id,))
        lvl = db_object.fetchone()[0]
        daily_count = 'SELECT daily FROM users WHERE id = %s'
        db_object.execute(daily_count, (message.chat.id,))
        daily_count = db_object.fetchone()[0]
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
        exp_reward = math.ceil(full_exp_day / daily_count)
        print(exp_reward)
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
        money_upd = 'UPDATE users set primogems = primogems + %s WHERE id = %s'
        primo_reward = reward * random.randint(1, 10)
        db_object.execute(money_upd, (primo_reward, message.chat.id))
        stat_reward = random.random() * reward
        rank_exp_left_slt = "SELECT rank_exp_left FROM users WHERE id =%s"
        db_object.execute(rank_exp_left_slt, (message.chat.id, ))
        rank_exp_left = db_object.fetchone()[0]
        daily_left_slt = 'SELECT dailies_left FROM users WHERE id= %s'
        db_object.execute(daily_left_slt, (message.chat.id, ))
        daily_left_count = db_object.fetchone()[0]
        energy_left_slt = 'SELECT energy_left FROM users where id =%s'
        db_object.execute(energy_left_slt, (message.chat.id, ))
        energy_left = db_object.fetchone()[0]
        rank_exp_count = math.ceil(rank_exp_left / daily_left_count)
        energy_count = math.ceil(energy_left / daily_left_count)
        energy_update = 'UPDATE users SET energy = energy + %s WHERE id = %s AND energy < 1000'
        db_object.execute(energy_update, (energy_count, message.chat.id))
        energy_left_update = 'UPDATE users SET energy_left = energy_left - %s where id= %s'
        db_object.execute(energy_left_update, (energy_count, message.chat.id))
        rank_slt = 'SELECT rank FROM users WHERE id = %s'
        db_object.execute(rank_slt, (message.chat.id,))
        rank = db_object.fetchone()[0]
        rank_exp_update = 'UPDATE users SET rank_exp = rank_exp + %s WHERE id = %s RETURNING rank_exp'
        rank_exp_left_update = 'UPDATE users SET rank_exp_left = rank_exp_left - %s WHERE id=%s'
        db_object.execute(rank_exp_left_update, (rank_exp_count, message.chat.id))
        db_object.execute(rank_exp_update, (rank_exp_count, message.chat.id))
        new_rank_exp = db_object.fetchall()[0][0]
        if new_rank_exp > rank_dict[rank + 1]:
            rank_update = 'UPDATE users SET rank = rank + 1 WHERE id = %s'
            db_object.execute(rank_update, (message.chat.id,))
        await asyncio.sleep(1.5)
        await bot.delete_message(chat_id=message.chat.id, message_id=msg_to_delete.message_id)
        if typik.strip() == 'physics':
            upd = 'UPDATE stats SET physics = physics + %s WHERE id = %s'
            db_object.execute(upd, (stat_reward, message.chat.id))
            await bot.send_message(message.chat.id, f'daily completed.\n'
                                                    f'physics gain : {format(stat_reward, ".4f")}\n'
                                                    f'exp gain: {exp_reward}\n'
                                                    f'primo gain: {primo_reward}',
                                   reply_markup=daily_markup)
        elif typik.strip() == 'wisdom':
            upd = 'UPDATE stats SET wisdom = wisdom + %s WHERE id = %s'
            db_object.execute(upd, (stat_reward, message.chat.id))
            await bot.send_message(message.chat.id, f'daily completed.\n'
                                                    f'wisdom gain : {format(stat_reward, ".4f")}\n'
                                                    f'exp gain: {exp_reward}\n'
                                                    f'primo gain: {primo_reward}',
                                   reply_markup=daily_markup)
        else:
            upd = 'UPDATE stats SET intelligence = intelligence + %s WHERE id = %s'
            db_object.execute(upd, (stat_reward, message.chat.id))
            await bot.send_message(message.chat.id, f'daily completed.\n'
                                                    f'intelligence gain : {format(stat_reward, ".4f")}\n'
                                                    f'exp gain: {exp_reward}\n'
                                                    f'primo gain: {primo_reward}',
                                   reply_markup=daily_markup)
        upd = 'UPDATE users SET dailies_left = dailies_left - 1 WHERE id=%s'
        db_object.execute(upd, (message.chat.id, ))
        dlt = 'UPDATE dailies SET accomplishment = 1 WHERE id = %s AND info = %s '
        db_object.execute(dlt, (message.chat.id, info))
        db_object.execute(f'DELETE FROM dailies WHERE id={message.chat.id + 1}')
        db_connection.commit()

        await bot.set_state(message.chat.id, States.dailies_main)
    elif message.text.strip() == "No":
        await bot.set_state(message.chat.id, States.dailies_main)
        await bot.send_message(message.chat.id, 'Returning to dailies main', reply_markup=daily_markup)


@bot.callback_query_handler(func=None, config=additional_callback.filter())
async def additional_stats(call: types.CallbackQuery):
    if call.data == 'added:main':
        db_object.execute(f"SELECT nickname,lvl,exp FROM users WHERE id = {call.message.chat.id}")
        res = db_object.fetchall()
        rank = res[0][1]
        exp_needed = lvl_dict[rank + 1]
        db_object.execute(f'SELECT physics,wisdom,intelligence FROM stats WHERE id = {call.message.chat.id}')
        stati = db_object.fetchall()
        stats = f'👾 <b>{res[0][0].strip()}:</b>\n\n' \
                f'✨ <b>rank:</b> <em>{rank} ({res[0][2]}/{exp_needed})</em>\n' \
                f'⚔ <b>attack:</b> <em>none</em>\n' \
                f'🛡 <b>defence:</b><em> none</em>\n' \
                f'🛡 <b>physics:</b><em> {format(stati[0][0], ".4f")}</em>\n' \
                f'🛡 <b>wisdom:</b><em> {format(stati[0][1], ".4f")}</em>\n' \
                f'🛡 <b>intelligent:</b><em> {format(stati[0][2], ".4f")}</em>\n'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=stats, reply_markup=additional_markup, parse_mode='HTML')
    elif call.data == 'added:currency':
        await bot.answer_callback_query(call.id, cache_time=2)
        db_object.execute(f'SELECT primogems,dust,mora FROM users WHERE id={call.from_user.id}')
        result = db_object.fetchall()
        text = f'👾 <b>your currency:</b>\n\n💠 <b>primogems:</b> {result[0][0]}\n' \
               f'💫 <b>stardust:</b> {result[0][1]}\n🪙 <b>mora:</b> {result[0][2]}'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=text, reply_markup=additional_markup, parse_mode='HTML')
    elif call.data == 'added:rewards':
        await bot.answer_callback_query(call.id, cache_time=40)
        await bot.send_message(call.message.chat.id, 'Nothing is here yet', reply_markup=main_markup)
    elif call.data == 'added:setting':
        await bot.answer_callback_query(call.id, cache_time=40)
        await bot.send_message(call.message.chat.id, 'Nothing is here yet', reply_markup=main_markup)
    elif call.data == 'added:talents':
        await bot.answer_callback_query(call.id, cache_time=40)
        await bot.send_message(call.message.chat.id, 'Nothing is here yet', reply_markup=main_markup)
    elif call.data == 'added:back':
        await bot.answer_callback_query(call.id, cache_time=40)
        photo = open('images/main.jpg', 'rb')
        await bot.send_photo(chat_id=call.message.chat.id, photo=photo, reply_markup=main_markup)


@bot.callback_query_handler(func=None, config=wish_callback.filter())
async def banner_choose(call: types.CallbackQuery):
    if call.data == 'wish:primogems':
        await bot.answer_callback_query(call.id, cache_time=2)
        slt = 'SELECT primogems FROM users WHERE id =%s'
        db_object.execute(slt, (call.message.chat.id,))
        primo = db_object.fetchone()[0]
        banner = open('images/primobanner.jpg', 'rb')
        msg = await bot.edit_message_media(media=types.InputMedia(type='photo', media=banner),
                                           message_id=call.message.id,
                                           chat_id=call.from_user.id, reply_markup=primo_banner_markup)
        await bot.edit_message_caption(caption=f'cost is 20💠\nyou have {primo}💠',
                                       chat_id=call.message.chat.id, message_id=msg.message_id,
                                       reply_markup=primo_banner_markup)
    elif call.data == 'wish:dust':
        await bot.answer_callback_query(call.id, cache_time=40)
        await bot.send_message(call.message.chat.id, 'nothing is here yet..', reply_markup=main_markup)
    elif call.data == 'wish:mora':
        await bot.answer_callback_query(call.id, cache_time=40)
        await bot.send_message(call.message.chat.id, 'nothing is here yet...', reply_markup=main_markup)
    elif call.data == 'wish:back':
        photo = open('images/main.jpg', 'rb')
        await bot.send_photo(photo=photo, chat_id=call.message.chat.id, reply_markup=main_markup)
        await bot.set_state(call.message.chat.id, States.main, call.message.chat.id)


@bot.callback_query_handler(func=None, config=primo_banner_callback.filter())
async def wishing(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id, cache_time=5)
    if call.data == 'banner1:roll':
        slt = 'SELECT primogems FROM users WHERE id=%s'
        db_object.execute(slt, (call.message.chat.id,))
        if db_object.fetchone()[0] > 20:
            upd = 'UPDATE users SET primogems = primogems - 20 WHERE id= %s'
            db_object.execute(upd, (call.message.chat.id,))
            upd = 'UPDATE users SET dust = dust + 15 WHERE id= %s'
            db_object.execute(upd, (call.message.chat.id,))
            drop = open('images\drop.jpg', 'rb')
            outcome = wish_processing('primogems')
            reward = wish_reward('primogems', outcome)
            db_object.execute(f'SELECT nickname FROM users WHERE id={call.from_user.id}')
            nickname = db_object.fetchone()[0].strip()
            if outcome == 5:
                animation = open('images/video/5starpull.mp4', 'rb')
                msg5 = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                    message_id=call.message.id,
                                                    media=types.InputMedia(type='animation', media=animation))
                await bot.edit_message_caption(caption=f'{nickname} is rolling gacha', chat_id=call.from_user.id,
                                               message_id=msg5.message_id)
                await asyncio.sleep(7)
                msg = await bot.edit_message_media(media=types.InputMediaPhoto(media=drop), chat_id=call.from_user.id,
                                                   message_id=msg5.message_id)
                await bot.edit_message_caption(caption=f'You got {reward}\n'
                                                       f'and a little of 15 dust', chat_id=call.from_user.id,
                                               message_id=msg.message_id, reply_markup=primo_banner_markup)
                db_object.execute(f'INSERT INTO inventory(info,id,rarity) VALUES (%s,%s,%s)',
                                  (reward, call.from_user.id,
                                   outcome))
                db_connection.commit()
            elif outcome == 4:
                animation = open('images/video/4starpull.mp4', 'rb')
                msg4 = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                    message_id=call.message.id,
                                                    media=types.InputMedia(type='animation', media=animation))
                await bot.edit_message_caption(caption=f'{nickname} is rolling gacha', chat_id=call.from_user.id,
                                               message_id=msg4.message_id)
                await asyncio.sleep(7)
                msg = await bot.edit_message_media(media=types.InputMediaPhoto(media=drop), chat_id=call.from_user.id,
                                                   message_id=msg4.message_id)
                await bot.edit_message_caption(caption=f'You got {reward}\n'
                                                       f'and a little of 15 dust', chat_id=call.from_user.id,
                                               message_id=msg.message_id, reply_markup=primo_banner_markup)
                db_object.execute(f'INSERT INTO inventory(info,id,rarity) VALUES (%s,%s,%s)',
                                  (reward, call.from_user.id,
                                   outcome))
                db_connection.commit()
            elif outcome == 3:
                animation = open('images/video/3starpull.mp4', 'rb')
                msg3 = await bot.edit_message_media(chat_id=call.message.chat.id,
                                                    message_id=call.message.id,
                                                    media=types.InputMedia(type='animation', media=animation))
                await bot.edit_message_caption(caption=f'{nickname} is rolling gacha', chat_id=call.from_user.id,
                                               message_id=msg3.message_id)
                await asyncio.sleep(7)
                msg = await bot.edit_message_media(media=types.InputMediaPhoto(media=drop), chat_id=call.from_user.id,
                                                   message_id=msg3.message_id)
                await bot.edit_message_caption(caption=f'You got {reward}\n'
                                                       f'and a little of 15 dust', chat_id=call.from_user.id,
                                               message_id=msg.message_id, reply_markup=primo_banner_markup)
                db_object.execute(f'INSERT INTO inventory(info,id,rarity) VALUES (%s,%s,%s)',
                                  (reward, call.from_user.id,
                                   outcome))
                db_connection.commit()
        else:
            wishing_photo = open('images/main_wish.jpg', 'rb')
            msg = await bot.edit_message_media(media=types.InputMedia(type='photo', media=wishing_photo),
                                               message_id=call.message.id,
                                               chat_id=call.from_user.id, reply_markup=wish_markup)
            await bot.edit_message_caption(caption=f'you have no money, go work you bastard', chat_id=call.from_user.id,
                                           message_id=msg.message_id, reply_markup=wish_markup)

    elif call.data == 'banner1:back':
        wishing_photo = open('images/main_wish.jpg', 'rb')
        await bot.edit_message_media(media=types.InputMedia(type='photo', media=wishing_photo),
                                     message_id=call.message.id,
                                     chat_id=call.from_user.id, reply_markup=wish_markup)


@bot.callback_query_handler(func=None, config=storage_callback.filter())
async def inventoring(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id, cache_time=1)
    if call.data == 'storage:life':
        db_object.execute(f'SELECT info FROM inventory WHERE id={call.message.chat.id} AND rarity=5')
        inventory = db_object.fetchall()
        show_inventory = ''
        for item in inventory:
            show_inventory += item[0] + '\n'
        await bot.edit_message_text(chat_id=call.message.chat.id, text=f'inventory:\n{show_inventory}',
                                    reply_markup=life_inventory_rare_epic_markup, message_id=call.message.message_id)
    elif call.data == 'storage:game':
        await bot.send_message(call.message.chat.id, 'Nothing is here yet', reply_markup=main_markup)
    elif call.data == 'storage:back':
        photo = open('images/main.jpg', 'rb')
        await bot.send_photo(photo=photo, chat_id=call.message.chat.id, reply_markup=main_markup)
        await bot.set_state(call.message.chat.id, States.main, call.message.chat.id)


@bot.callback_query_handler(func=None, config=life_inventory_callback.filter())
async def life_inventory(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id, cache_time=1)
    show_inventory = ''
    try:
        if call.data == 'life_item_rarity:rare':
            db_object.execute(f'SELECT info FROM inventory WHERE id={call.message.chat.id} AND rarity=3')
            inventory = db_object.fetchall()
            for item in inventory:
                show_inventory += item[0] + '\n'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f'inventory:\n{show_inventory}',
                                        reply_markup=life_inventory_legendary_epic_markup)
        elif call.data == 'life_item_rarity:epic':
            db_object.execute(f'SELECT info FROM inventory WHERE id={call.message.chat.id} AND rarity=4')
            inventory = db_object.fetchall()
            for item in inventory:
                show_inventory += item[0] + '\n'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f'inventory:\n{show_inventory}',
                                        reply_markup=life_inventory_rare_legendary_markup)
        elif call.data == 'life_item_rarity:legendary':
            db_object.execute(f'SELECT info FROM inventory WHERE id={call.message.chat.id} AND rarity=5')
            inventory = db_object.fetchall()
            for item in inventory:
                show_inventory += item[0] + '\n'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f'inventory:\n{show_inventory}',
                                        reply_markup=life_inventory_rare_epic_markup)
        elif call.data == 'life_item_rarity:use':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='something',
                                        reply_markup=life_inventory_use_markup)
        elif call.data == 'life_item_rarity:back':
            await bot.edit_message_text(text='you got to the storage which box should we open?',
                                        reply_markup=storage_markup, chat_id=call.message.chat.id,
                                        message_id=call.message.message_id)
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=None, config=life_inventory_use_callback.filter())
async def inventory_using(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id, cache_time=1)
    if call.data == 'life_use:back':
        show_inventory = ''
        db_object.execute(f'SELECT info FROM inventory WHERE id={call.message.chat.id} AND rarity=3')
        inventory = db_object.fetchall()
        for item in inventory:
            show_inventory += item[0] + '\n'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=f'inventory:\n{show_inventory}',
                                    reply_markup=life_inventory_legendary_epic_markup)
    elif call.data == 'life_use:rare':
        inventory_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        db_object.execute(f'SELECT info FROM inventory WHERE id={call.message.chat.id} AND rarity=3')
        inventory = db_object.fetchall()
        if inventory:
            item_list = []
            for item in inventory:
                item_list.append(types.KeyboardButton(text=item[0].strip()))
            for smt in range(0, len(item_list), 2):
                if smt != len(item_list) - len(item_list) % 2:
                    inventory_markup.add(item_list[smt], item_list[smt + 1])
                else:
                    if len(item_list) % 2 == 0:
                        inventory_markup.add(item_list[smt], item_list[smt + 1])
                    else:
                        inventory_markup.add(item_list[smt])
            await bot.send_message(chat_id=call.message.chat.id, text='choose an item', reply_markup=inventory_markup)
            await bot.set_state(chat_id=call.message.chat.id, state=States.life_inventory_using,
                                user_id=call.message.chat.id)
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, text='nothing is here,work more!',
                                        reply_markup=storage_markup, message_id=call.message.message_id)
    elif call.data == 'life_use:epic':
        inventory_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        db_object.execute(f'SELECT info FROM inventory WHERE id={call.message.chat.id} AND rarity=4')
        inventory = db_object.fetchall()
        if inventory:
            for item in inventory:
                inventory_markup.add(types.KeyboardButton(text=item[0].strip()))
            await bot.send_message(chat_id=call.message.chat.id, text='choose an item', reply_markup=inventory_markup)
            await bot.set_state(chat_id=call.message.chat.id, state=States.life_inventory_using,
                                user_id=call.message.chat.id)
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, text='nothing is here,work more!',
                                        reply_markup=storage_markup, message_id=call.message.message_id)
    elif call.data == 'life_use:legendary':
        inventory_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        db_object.execute(f'SELECT info FROM inventory WHERE id={call.message.chat.id} AND rarity=5')
        inventory = db_object.fetchall()
        if inventory:
            item_list = []
            for item in inventory:
                item_list.append(types.KeyboardButton(text=item[0].strip()))
            for smt in range(0, len(item_list), 2):
                if smt != len(item_list) - len(item_list) % 2:
                    inventory_markup.add(item_list[smt], item_list[smt + 1])
                else:
                    if len(item_list) % 2 == 0:
                        pass
                    else:
                        inventory_markup.add(item_list[smt])
            await bot.send_message(chat_id=call.message.chat.id, text='choose an item', reply_markup=inventory_markup)
            await bot.set_state(chat_id=call.message.chat.id, state=States.life_inventory_using,
                                user_id=call.message.chat.id)
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, text='nothing is here,work more!',
                                        reply_markup=storage_markup, message_id=call.message.message_id)


@bot.message_handler(state=States.life_inventory_using)
async def inventory_item_used(message):
    dlt = 'DELETE FROM inventory WHERE ctid in(select ctid from inventory where info = %s LIMIT 1)'
    db_object.execute(dlt, (message.text,))
    db_connection.commit()
    await bot.send_message(chat_id=message.chat.id, text=f'{message.text.strip()} got successfully used',
                           reply_markup=life_inventory_use_markup)
    await bot.set_state(chat_id=message.chat.id, state=States.main, user_id=message.chat.id)


async def listener(messages):
    for m in messages:
        print(f'Current state is: {await bot.get_state(m.from_user.id, m.chat.id)}')


async def main():
    await asyncio.gather(bot.infinity_polling(), dailie_reset())


bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(CallbackFilter())
bot.set_update_listener(listener)

if __name__ == '__main__':
    asyncio.run(main())
