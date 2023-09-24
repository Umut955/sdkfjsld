from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from dotenv import load_dotenv
import os
import random

start_text = """
версия 0.1 alpha.
Приветствую, друг! 🐾 Добро пожаловать в мир Wild Craft! 🌿

Я - твой гид и проводник в этом удивительном мире. 🌍 Перед нами открывается захватывающее приключение, где ты сможешь проверить свои знания об игре Wild Craft.

я отправлю тебе первый тест, состоящий из текста или картинок.

Не переживай, вопросы будут снабжены инлайн-кнопками с вариантами ответов. Тебе всего лишь нужно будет нажать на одну из кнопок, чтобы дать свой ответ. 🤖💡

За каждый правильный ответ ты будешь получать баллы и переходить к следующему вопросу. По окончании теста ты узнаешь, насколько ты знаешь мир Wild Craft. 🌟

Не забудь подписаться на наш канал __MovieSize__, чтобы быть в курсе всех обновлений и видеороликов о нашем боте! 📽️📢

Погнали в путешествие по Wild Craft! 🐺🌿"""

admin_start_text = """
версия 0.1 alpha.
Добро пожаловать, администратор! 🤖👑

Рад видеть вас в роли управляющего этим ботом. Ваш статус
администратора открывает перед вами новые возможности для управления и проверки бота.
Вам доступны следующие действия:

🔘 Пропускать вопросы
🔘 Выдавать себе баллы
🔘 Переноситься на любые вопросы
🔘 Проверять отзывы и многое другое!

Напоминаем, что админ-панель создана исключительно для тестирования бота,
и мы просим вас использовать её только в честных целях.
Спасибо за ваше участие в развитии и улучшении нашего бота! 🌟🤝"""



load_dotenv()

start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(KeyboardButton('начать'))
start_play_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_play_kb.add(KeyboardButton('1'), KeyboardButton('2'), KeyboardButton('3'), KeyboardButton('4'))
play_kb = ReplyKeyboardMarkup(resize_keyboard=True)
play_kb.add(KeyboardButton('1'), KeyboardButton('2'), KeyboardButton('3'), KeyboardButton('4'))

# админские клавиатуры ===============================

admin_start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_start_kb.add(KeyboardButton('начать'),
                   KeyboardButton('переключится на вопрос🛡️'),
                   KeyboardButton('убрать админку для этого сеанса🛡️'),
                   KeyboardButton('выдать баллы🛡️'),
                   KeyboardButton('отзывы🛡️ (в процессе)'))
admin_start_play_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_start_play_kb.add(KeyboardButton('1'), KeyboardButton('2'), KeyboardButton('3'), KeyboardButton('4'), KeyboardButton('пропустить🛡️'))
admin_play_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_play_kb.add(KeyboardButton('1'), KeyboardButton('2'), KeyboardButton('3'), KeyboardButton('4'), KeyboardButton('пропустить🛡️'))
admin_skip_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_skip_kb.add(KeyboardButton('на 1🛡️'),
                  KeyboardButton('на 2🛡️'),
                  KeyboardButton('на 3🛡️'),
                  KeyboardButton('на 4🛡️'),
                  KeyboardButton('на 5🛡️'),
                  KeyboardButton('на 6🛡️'),
                  KeyboardButton('на 7🛡️'),
                  KeyboardButton('на 8🛡️'),
                  KeyboardButton('на 9🛡️'),
                  KeyboardButton('на 10🛡️'),
                  KeyboardButton('на 11🛡️'),
                  KeyboardButton('на 12🛡️'),
                  KeyboardButton('на 13🛡️'),
                  KeyboardButton('на 14🛡️'),
                  KeyboardButton('на 15🛡️'),)
admin_balls_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_balls_kb.add(KeyboardButton('+1🛡️'),
                  KeyboardButton('+5🛡️'),
                  KeyboardButton('+10🛡️'),
                  KeyboardButton('начать'))


admin = False
bot = Bot((os.getenv('TOKEN_API')))
dp = Dispatcher(bot)
admin_ids = [int(id) for id in os.getenv('ADMIN_IDS').split(',')]
question_num = 1
balls = 0
question_list = ['в каком году появился Вайлд крафт в google play?\n 1. 2010 2. 2016 3. 2018 4. 2015',
                 'сколько боссов в игре? включая океан мир и клановых\n 1. 27 2. 20 3. 32 4. 23',
                 'какая вещь из них дороже?\n 1. логово (плавучие острова) 2. приятель 3. легендарный скин на персонажа 4. легендарный скин в океан мире',
                 'сколько хп у Гигантского медведя в онлайне?\n 1. 8000 2. 7500 3. 7000 4. 7250',
                 'что нужно сделать чтобы получить ранг мастер?\n 1. 3 животное до 100 2. 2 животное до 120 3. 1 животное до 200 4. 2 животное до 150',
                 'на сколько процентов вырастает количество опыта с клубом?\n 1. 100 2. 200 3. 120 4. 25',
                 'кто из этих животных не является питомцем?\n 1. скорпион 2. оцелот 3. цербер 4. слон',
                 'что такое "аура" у приятелей?\n 1. эффект действует и на игроков рядом 2. работает непрерывно 3. вокруг игрока щит 4. эффект не действует на вас пока не включена аура',
                 'кто из этих ютуберов снимает вайлд?\n 1. Nifty 2. Ландау 3. Дом кека 4. Шилки',
                 'какой сезон пасса в обнове с кенгуру?\n 1. 4 2. 5 3. 6 4. 7',
                 'сколько траснформаций в игре? (было в обнове с кенгуру)\n 1. 8 2. 9 3. 5 4. 12',
                 'сколько животных в игре? (в обнове с кенгуру)\n 1. 11 2. 9 3. 12 4. 14',
                 'когда дают еженедельный сундук клуба?\n 1. в понедельник 2. в среду 3. в воскресенье 4. в субботу',
                 'какие животные были в самой первой версий?\n 1. волк, лиса, рысь 2. волк 3. волк, лиса 4. лиса',
                 'максимальное количество орехов\n 1. 9.999 2. 4.999 3. 999 4. 5.999', '0']
true_answers_list = [3, 1, 2, 1, 4, 1, 2, 1, 4, 3, 2, 3, 4, 1, 4]
True_list = ['точно!', 'да, правильно!', 'ого! Прям в точку!', 'ктото заслужил баллы)', 'умничка!']


@dp.message_handler(commands=['start'])
async def start_text_add(message: types.Message):
    global admin, question_num
    question_num = 1
    if message.from_user.id in admin_ids:
        await message.reply(text=admin_start_text, reply_markup=admin_start_kb)
        admin = True
    else:
        await message.reply(text=start_text, reply_markup=start_kb)

@dp.message_handler(commands=['id'])
async def print_id(message: types.Message):
    await message.reply(text=f'{message.from_user.id}')

@dp.message_handler(text='начать')
async def new_play(message: types.Message):
    global admin
    if message.from_user.id in admin_ids and admin:
        await message.answer(text=question_list[question_num - 1], reply_markup=admin_start_play_kb)
    else:
        await message.answer(text=question_list[question_num - 1], reply_markup=start_play_kb)


@dp.message_handler(text='1')
async def one(message: types.Message):
    global question_num, balls
    if question_num != 15:
        if message.from_user.id in admin_ids and admin:
            if 1 == true_answers_list[question_num - 1]:
                question_num += 1
                balls += 10
                await message.answer(
                    text=f'{True_list[random.randint(0, 4)]} \n ты получаешь 10 баллов! \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=admin_play_kb)
            else:
                question_num += 1
                await message.answer(
                    text=f'получится в следуйщий раз) \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=admin_play_kb)
        else:
            if 1 == true_answers_list[question_num - 1]:
                question_num += 1
                balls += 10
                await message.answer(
                    text=f'{True_list[random.randint(0, 4)]} \n ты получаешь 10 баллов! \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=play_kb)
            else:
                question_num += 1
                await message.answer(
                    text=f'получится в следуйщий раз) \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=play_kb)
    else:
        print(f'пользователь {message.from_user} получил {balls} баллов!')
        await message.answer(
            text=f'а вот и закончился наш тест в будущем будет больше тестов но пока что всё \n у тебя баллов {balls}!')
        if 0 <= balls and 20 >= balls:
            await message.answer(text=f'твой уровень: нуб. Брат надо играть.')

        elif 21 <= balls and 40 >= balls:
            await message.answer(text=f'твой уровень: начинающий. Удачи в начинаниях!.')

        elif 41 <= balls and 60 >= balls:
            await message.answer(text=f'твой уровень: норм. ну что-то среднее.')

        elif 61 <= balls and 80 >= balls:
            await message.answer(text=f'твой уровень: норм+. чуть больше среднего.')

        elif 81 <= balls and 110 >= balls:
            await message.answer(text=f'твой уровень: хорош. сразу видно не один день играешь.')

        elif 111 <= balls and 130 >= balls:
            await message.answer(text=f'твой уровень: профи. много всего повидал.')

        elif 131 <= balls and 150 >= balls:
            await message.answer(text=f'твой уровень: максимум. идеальный результат могу тебя поздравить.')

        else:
            await message.answer(text=f'произошла ошибка. Мы не смогли оценить уровень твоих знаний. Возможно у вас баллы не в пределах 0/150.')
@dp.message_handler(text='2')
async def two(message: types.Message):
    global question_num, balls
    if question_num != 15:
        if message.from_user.id in admin_ids and admin:
            if 2 == true_answers_list[question_num - 1]:
                question_num += 1
                balls += 10
                await message.answer(
                    text=f'{True_list[random.randint(0, 4)]} \n ты получаешь 10 баллов! \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=admin_play_kb)
            else:
                question_num += 1
                await message.answer(
                    text=f'получится в следуйщий раз) \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=admin_play_kb)
        else:
            if 1 == true_answers_list[question_num - 1]:
                question_num += 1
                balls += 10
                await message.answer(
                    text=f'{True_list[random.randint(0, 4)]} \n ты получаешь 10 баллов! \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=play_kb)
            else:
                question_num += 1
                await message.answer(
                    text=f'получится в следуйщий раз) \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=play_kb)
    else:
        print(f'пользователь {message.from_user} получил {balls} баллов!')
        await message.answer(
            text=f'а вот и закончился наш тест в будущем будет больше тестов но пока что всё \n у тебя баллов {balls}!')
        if 0 <= balls and 20 >= balls:
            await message.answer(text=f'твой уровень: нуб. Брат надо играть.')

        elif 21 <= balls and 40 >= balls:
            await message.answer(text=f'твой уровень: начинающий. Удачи в начинаниях!.')

        elif 41 <= balls and 60 >= balls:
            await message.answer(text=f'твой уровень: норм. ну что-то среднее.')

        elif 61 <= balls and 80 >= balls:
            await message.answer(text=f'твой уровень: норм+. чуть больше среднего.')

        elif 81 <= balls and 110 >= balls:
            await message.answer(text=f'твой уровень: хорош. сразу видно не один день играешь.')

        elif 111 <= balls and 130 >= balls:
            await message.answer(text=f'твой уровень: профи. много всего повидал.')

        elif 131 <= balls and 150 >= balls:
            await message.answer(text=f'твой уровень: максимум. идеальный результат могу тебя поздравить.')

        else:
            await message.answer(text=f'произошла ошибка. Мы не смогли оценить уровень твоих знаний. Возможно у вас баллы не в пределах 0/150.')

@dp.message_handler(text='3')
async def three(message: types.Message):
    global question_num, balls
    if question_num != 15:
        if message.from_user.id in admin_ids and admin:
            if 3 == true_answers_list[question_num - 1]:
                question_num += 1
                balls += 10
                await message.answer(
                    text=f'{True_list[random.randint(0, 4)]} \n ты получаешь 10 баллов! \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=admin_play_kb)
            else:
                question_num += 1
                await message.answer(
                    text=f'получится в следуйщий раз) \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=admin_play_kb)
        else:
            if 1 == true_answers_list[question_num - 1]:
                question_num += 1
                balls += 10
                await message.answer(
                    text=f'{True_list[random.randint(0, 4)]} \n ты получаешь 10 баллов! \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=play_kb)
            else:
                question_num += 1
                await message.answer(
                    text=f'получится в следуйщий раз) \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=play_kb)
    else:
        print(f'пользователь {message.from_user} получил {balls} баллов!')
        await message.answer(
            text=f'а вот и закончился наш тест в будущем будет больше тестов но пока что всё \n у тебя баллов {balls}!')
        if 0 <= balls and 20 >= balls:
            await message.answer(text=f'твой уровень: нуб. Брат надо играть.')

        elif 21 <= balls and 40 >= balls:
            await message.answer(text=f'твой уровень: начинающий. Удачи в начинаниях!.')

        elif 41 <= balls and 60 >= balls:
            await message.answer(text=f'твой уровень: норм. ну что-то среднее.')

        elif 61 <= balls and 80 >= balls:
            await message.answer(text=f'твой уровень: норм+. чуть больше среднего.')

        elif 81 <= balls and 110 >= balls:
            await message.answer(text=f'твой уровень: хорош. сразу видно не один день играешь.')

        elif 111 <= balls and 130 >= balls:
            await message.answer(text=f'твой уровень: профи. много всего повидал.')

        elif 131 <= balls and 150 >= balls:
            await message.answer(text=f'твой уровень: максимум. идеальный результат могу тебя поздравить.')

        else:
            await message.answer(text=f'произошла ошибка. Мы не смогли оценить уровень твоих знаний. Возможно у вас баллы не в пределах 0/150.')

@dp.message_handler(text='4')
async def four(message: types.Message):
    global question_num, balls
    if question_num != 15:
        if message.from_user.id in admin_ids and admin:
            if 4 == true_answers_list[question_num - 1]:
                question_num += 1
                balls += 10
                await message.answer(
                    text=f'{True_list[random.randint(0, 4)]} \n ты получаешь 10 баллов! \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=admin_play_kb)
            else:
                question_num += 1
                await message.answer(
                    text=f'получится в следуйщий раз) \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=admin_play_kb)
        else:
            if 1 == true_answers_list[question_num - 1]:
                question_num += 1
                balls += 10
                await message.answer(
                    text=f'{True_list[random.randint(0, 4)]} \n ты получаешь 10 баллов! \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=play_kb)
            else:
                question_num += 1
                await message.answer(
                    text=f'получится в следуйщий раз) \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                    reply_markup=play_kb)
    else:
        print(f'пользователь {message.from_user} получил {balls} баллов!')
        await message.answer(
            text=f'а вот и закончился наш тест в будущем будет больше тестов но пока что всё \n у тебя баллов {balls}!')
        if 0 <= balls and 20 >= balls:
            await message.answer(text=f'твой уровень: нуб. Брат надо играть.')

        elif 21 <= balls and 40 >= balls:
            await message.answer(text=f'твой уровень: начинающий. Удачи в начинаниях!.')

        elif 41 <= balls and 60 >= balls:
            await message.answer(text=f'твой уровень: норм. ну что-то среднее.')

        elif 61 <= balls and 80 >= balls:
            await message.answer(text=f'твой уровень: норм+. чуть больше среднего.')

        elif 81 <= balls and 110 >= balls:
            await message.answer(text=f'твой уровень: хорош. сразу видно не один день играешь.')

        elif 111 <= balls and 130 >= balls:
            await message.answer(text=f'твой уровень: профи. много всего повидал.')

        elif 131 <= balls and 150 >= balls:
            await message.answer(text=f'твой уровень: максимум. идеальный результат могу тебя поздравить.')

        else:
            await message.answer(text=f'произошла ошибка. Мы не смогли оценить уровень твоих знаний. Возможно у вас баллы не в пределах 0/150.')

# админ команды =========================================

@dp.message_handler(text='переключится на вопрос🛡️')
async def switch_quest(message: types.Message):
    global admin
    if message.from_user.id in admin_ids and admin:
        await message.answer(text='выберите на какой вопрос переключится...', reply_markup=admin_skip_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='убрать админку для этого сеанса🛡️')
async def switch_quest(message: types.Message):
    global admin
    if message.from_user.id in admin_ids and admin:
        admin = False
        await message.answer(text='теперь вы официально не админ)', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='выдать баллы🛡️')
async def switch_quest(message: types.Message):
    global admin, balls
    if message.from_user.id in admin_ids and admin:
        await message.answer(text='сколько баллов хотите добавить?', reply_markup=admin_balls_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='пропустить🛡️')
async def switch_quest(message: types.Message):
    global admin, balls, question_num
    if message.from_user.id in admin_ids and admin:
        if question_num != 15:
            question_num += 1
            balls += 10
            await message.answer(
                text=f'{True_list[random.randint(0, 4)]} \n ты получаешь 10 баллов! \n вопрос номер {question_num}: {question_list[question_num - 1]}',
                reply_markup=admin_play_kb)
        else:
            await message.answer(
                text=f'а вот и закончился наш тест в будущем будет больше тестов но пока что всё \n у тебя баллов {balls}!')
            if 0 <= balls and 20 >= balls:
                await message.answer(text=f'твой уровень: нуб. Брат надо играть.')

            elif 21 <= balls and 40 >= balls:
                await message.answer(text=f'твой уровень: начинающий. Удачи в начинаниях!.')

            elif 41 <= balls and 60 >= balls:
                await message.answer(text=f'твой уровень: норм. ну что-то среднее.')

            elif 61 <= balls and 80 >= balls:
                await message.answer(text=f'твой уровень: норм+. чуть больше среднего.')

            elif 81 <= balls and 110 >= balls:
                await message.answer(text=f'твой уровень: хорош. сразу видно не один день играешь.')

            elif 111 <= balls and 130 >= balls:
                await message.answer(text=f'твой уровень: профи. много всего повидал.')

            elif 131 <= balls and 150 >= balls:
                await message.answer(text=f'твой уровень: максимум. идеальный результат могу тебя поздравить.')

            else:
                await message.answer(
                    text=f'произошла ошибка. Мы не смогли оценить уровень твоих знаний. Возможно у вас баллы не в пределах 0/150.')
    else:
        await message.answer(text='бро, тебе явно не сюда.')

# мусорка =====================================================

@dp.message_handler(text='на 1🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 1
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 2🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 2
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 3🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 3
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 4🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 4
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 5🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 5
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 6🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 6
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 7🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 7
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 8🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 8
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 9🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 9
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 10🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 10
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 11🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 11
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 12🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 12
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 13🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 13
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 14🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 14
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler(text='на 15🛡️')
async def switch(message: types.Message):
    global admin, question_num
    if message.from_user.id in admin_ids and admin:
        question_num = 15
        await message.answer(text='успешно!', reply_markup=admin_start_kb)
    else:
        await message.answer(text='бро, тебе явно не сюда.')


@dp.message_handler(text='+1🛡️')
async def switch(message: types.Message):
    global admin, balls
    if message.from_user.id in admin_ids and admin:
        balls += 1
        await message.answer(text=f'успешно! у вас баллов: {balls}')
    else:
        await message.answer(text='бро, тебе явно не сюда.')
@dp.message_handler(text='+5🛡️')
async def switch(message: types.Message):
    global admin, balls
    if message.from_user.id in admin_ids and admin:
        balls += 5
        await message.answer(text=f'успешно! у вас баллов: {balls}')
    else:
        await message.answer(text='бро, тебе явно не сюда.')
@dp.message_handler(text='+10🛡️')
async def switch(message: types.Message):
    global admin, balls
    if message.from_user.id in admin_ids and admin:
        balls += 10
        await message.answer(text=f'успешно! у вас баллов: {balls}')
    else:
        await message.answer(text='бро, тебе явно не сюда.')

@dp.message_handler()
async def text(message: types.Message):
    await message.answer(text="я тебя не пон...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
