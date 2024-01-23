import telebot
from telebot import types
from config import TOKEN, greeting, answer_choice
from classes import User


bot = telebot.TeleBot(TOKEN)

user = User()
gen = user.quiz()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton('НАЧАТЬ')
    site = types.KeyboardButton('Контакты')
    markup.row(start_button, site)
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    global gen, user
    print(message.text)
    if message.text == 'Контакты':
        contacts(message)
        bot.register_next_step_handler(message, on_click)
    elif message.text == 'Оставить отзыв':
        bot.send_message(message.chat.id, 'Напишите, понравился ли вам бот '
                                          'или оставьте пожелания как его можно улучшить!')
        bot.register_next_step_handler(message, fitback)
    elif message.text == 'НАЧАТЬ' or 'Ещё раз':
        print('начало викторины')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Контакты'))
        bot.send_message(message.chat.id, 'Викторина состоит из 15 вопросов, '
                                          'в конце вам предоставится ваше тотемное животное', reply_markup=markup)
        user = User()
        gen = user.quiz()
        vict(message)
    else:
        pass


@bot.message_handler(content_types=['text'])
def contacts(message):
    if message.text == 'Контакты':
        markup_site = types.InlineKeyboardMarkup(row_width=2)
        website = types.InlineKeyboardButton('Перейти на вебсайт', url='https://moscowzoo.ru/')
        telegram = types.InlineKeyboardButton('Перейти в телеграм канал', url='https://t.me/Moscowzoo_official')
        markup_site.add(website, telegram)
        bot.send_message(message.chat.id, 'контакты зоопарка:', reply_markup=markup_site)


def vict(message):
    markup = types.InlineKeyboardMarkup()
    try:
        question = next(gen)
        answers = next(gen)
    except StopIteration:
        result(message)
    else:
        for answer, choice in answers.items():
            markup.add(types.InlineKeyboardButton(answer, callback_data=choice))
        bot.send_message(message.chat.id, question, reply_markup=markup)


def result(message):
    totemic_animals = user.result_func()
    text = f'Ваше тотемное животное: {totemic_animals}'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Ещё раз')
    btn2 = types.KeyboardButton('контакты')
    btn3 = types.KeyboardButton('Оставить отзыв')
    markup.add(btn1, btn2, btn3)
    with open(f'./image/{totemic_animals}.jpg', 'rb') as image:
        bot.send_photo(message.chat.id, image, caption=text, reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    print(call.data)
    user.add_answer(call.data)
    vict(call.message)


def fitback(message):
    with open('./feedbacks/feedbacks.txt', 'a') as file:
        file.write(message.text + '\n')
    bot.reply_to(message, 'Спасибо за отзыв!')
    bot.register_next_step_handler(message, on_click)


bot.polling(non_stop=True)
