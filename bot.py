import telebot
from telebot import types

from credentials import config
from mygithub import MetOptRepo
from itmotable import ItmoTable
import itmotable
import logging


bot = telebot.TeleBot(config.bot_token)

logging.basicConfig(format='%(levelname)s | %(asctime)s | %(funcName)s | %(lineno)d | %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='utils/bot.log',
                    encoding='utf-8',
                    level=logging.INFO)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    pass


@bot.message_handler(commands=['help'])
def send_welcome(message):
    pass


@bot.message_handler(commands=['commit'])
def commit(message):
    logging.info(f'{message.from_user.username} | {message.text}')
    process_printing_commits_step(message, n=1)


@bot.message_handler(commands=['3commits'])
def commits(message):
    logging.info(f'{message.from_user.username} | {message.text}')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(*MetOptRepo.team.keys(), 'всех')
    msg = bot.reply_to(message, 'Чьи коммиты посмотрим?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_printing_commits_step, n=3)


def process_printing_commits_step(message, n: int):
    logging.info(f'{message.from_user.username} | {message.text}')
    repo = MetOptRepo()
    commits = repo.commits_to_str(message.text, n)
    bot.send_message(message.chat.id, commits)


@bot.message_handler(commands=['itmotable'])
def itmo_table(message):
    logging.info(f'{message.from_user.username} | {message.text}')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Последнюю готовую', 'Новую')
    file_name = ItmoTable.get_last_table_name(ItmoTable.get_last_table())
    msg = bot.reply_to(message, f'Взять \n'
                                f'{file_name} \n'
                                f'или сделать новую?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_send_itmo_table_step)


def process_send_itmo_table_step(message):
    log_message = f'{message.from_user.username} | {message.text}'
    logging.info(log_message)
    if message.text == 'Последнюю готовую':
        pass
    elif message.text == 'Новую':
        tmp = bot.reply_to(message, 'Тогда подожди немного...')
        try:
            ItmoTable().collect_all_subjects().delete_dead_students(20).sort().to_csv()
        except itmotable.HttpError:
            bot.send_message(message.chat.id, "Проблема с Google Sheets API.\n"
                                              "Отправлю пока последнюю созданную таблицу.")
            logging.error(log_message)
        finally:
            bot.delete_message(tmp.chat.id, tmp.message_id)
    else:
        bot.reply_to(message, 'Тебе всего лишь надо было на кнопку нажать')
        logging.warning(log_message)
        return
    file = open(ItmoTable.get_last_table(), 'rb')
    bot.send_document(message.chat.id, file)
    file.close()


bot.infinity_polling()
