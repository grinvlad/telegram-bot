import itmotable

from credentials import config
import os
import telebot
import requests
import json

from itmotable import ItmoTable

OWNER_REPO = 'grinvlad'
REPO = 'optimization-methods'
bot = telebot.TeleBot(config.bot_token)

# headers just to show that I'm not a bot
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
              'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}


def get_commits():
    req = requests.get(f'https://api.github.com/repos/{OWNER_REPO}/{REPO}/commits', headers=headers)
    src = req.text
    all_commits = json.loads(src)
    return all_commits


def commit_to_str(commit):
    s = f"message:   '{commit['commit']['message']}'\n" \
          f"author:    {commit['author']['login']}\n" \
          f"date:    {commit['commit']['author']['date'].replace('T', '  ')[:-4]}"
    return s


@bot.message_handler(commands=['start'])
def send_welcome(message):
    pass


@bot.message_handler(commands=['help'])
def send_welcome(message):
    pass


@bot.message_handler(commands=['lastcommit'])
def print_last_commit(message):
    last_commit = get_commits()[0]
    bot.send_message(message.chat.id, commit_to_str(last_commit))


@bot.message_handler(commands=['last3commits'])
def print_last_three_commits(message):
    commits = get_commits()[:3]
    s = commit_to_str(commits[2]) + '\n\n\n' + commit_to_str(commits[1]) + '\n\n\n' + commit_to_str(commits[0])
    bot.send_message(message.chat.id, s)


@bot.message_handler(commands=['itmotable'])
def send_itmo_table(message):
    tmp = bot.reply_to(message, "Придется подождать секунд 10...")
    try:
        ItmoTable().collect_all_subjects().delete_dead_students(20).to_csv()
    except itmotable.HttpError:
        bot.send_message(message.chat.id, "Sorry, something wrong with API")
    file = open(get_latest_file('itmo-tables-samples'), 'rb')
    bot.send_document(message.chat.id, file)
    bot.delete_message(message.chat.id, tmp.message_id)
    file.close()


def get_latest_file(dir_: str):
    paths = [os.path.join(os.path.abspath(os.getcwd() + "/" + dir_), file) for file in os.listdir(dir_)]
    latest_file = max(paths, key=os.path.getmtime)
    return latest_file


bot.infinity_polling()
