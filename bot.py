import telebot

import memes
import itmotable

from credentials import config
from mygithub import MetOptRepo
from itmotable import ItmoTable
from memes import MemeQue
from log import log


bot = telebot.TeleBot(config.bot_token)


@bot.message_handler(commands=['start'])
@log
def send_welcome(message):
    pass


@bot.message_handler(commands=['help'])
@log
def send_welcome(message):
    pass


@bot.message_handler(commands=['commit'])
@log
def commit(message):
    process_printing_commits_step(message, n=1)


@bot.message_handler(commands=['3commits'])
@log
def commits(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(*MetOptRepo.team.keys(), 'всех')
    msg = bot.reply_to(message, 'Чьи коммиты посмотрим?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_printing_commits_step, n=3)


def process_printing_commits_step(message, n: int):
    repo = MetOptRepo()
    commits_ = repo.commits_to_str(message.text, n)
    bot.send_message(message.chat.id, commits_)


@bot.message_handler(commands=['itmotable'])
@log
def itmo_table(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Последнюю готовую', 'Новую')
    file_name = itmotable.get_last_table_name(itmotable.get_last_table())
    msg = bot.reply_to(message, f'Взять \n'
                                f'{file_name} \n'
                                f'или сделать новую?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_send_itmo_table_step)


@log
def process_send_itmo_table_step(message):
    if message.text == 'Последнюю готовую':
        pass
    elif message.text == 'Новую':
        tmp = bot.reply_to(message, 'Тогда подожди немного...')
        try:
            ItmoTable().collect_all_subjects().delete_dead_students(20).sort().to_csv()
        except itmotable.ItmoTableException as e:
            bot.send_message(message.chat.id, str(e))
        finally:
            bot.delete_message(tmp.chat.id, tmp.message_id)
    else:
        bot.reply_to(message, 'Тебе всего лишь надо было на кнопку нажать')
        return
    file = open(itmotable.get_last_table(), 'rb')
    bot.send_document(message.chat.id, file)
    file.close()


@bot.message_handler(commands=['len_meme_queue'])
@log
def len_meme_queue(message):
    que = MemeQue()
    answer_message = f'Мемов в текущей очереди: {len(que)}'
    bot.reply_to(message, answer_message)


@bot.message_handler(chat_types=['private'], content_types=['text'], func=memes.when_to_add_new_meme)
def add_meme(message):
    url = message.text
    index = MemeQue().add_new_meme(url)
    answer_message = ('Добавила.\n'
                      f'Позиция мема в текущей очереди: {index}')
    bot.reply_to(message, answer_message)


@bot.message_handler(chat_types=['private'], content_types=['text'], func=memes.when_to_illegally_add_new_meme)
def illegally_add_meme(message):
    option, url = message.text.split(maxsplit=1)
    index = MemeQue().illegally_add_new_meme(url)
    answer_message = (f'Добавила c опцией {option}.\n'
                      f'Позиция мема в текущей очереди: {index}')
    bot.reply_to(message, answer_message)


@bot.message_handler(func=memes.when_to_send_meme)
@log
def send_next_meme(message):
    bot.send_photo(message.chat.id, MemeQue().get_next_meme())


bot.infinity_polling()
