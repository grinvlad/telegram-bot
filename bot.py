import config
import telebot
import requests
import json

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
    bot.reply_to(message, "Хуярт")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Хуелп")


@bot.message_handler(commands=['getlastcommit'])
def print_last_commit(message):
    last_commit = get_commits()[0]
    bot.send_message(message.chat.id, commit_to_str(last_commit))


@bot.message_handler(commands=['getlastthreecommits'])
def print_last_three_commits(message):
    commits = get_commits()[:3]
    s = commit_to_str(commits[2]) + '\n\n\n' + commit_to_str(commits[1]) + '\n\n\n' + commit_to_str(commits[0])
    bot.send_message(message.chat.id, s)


@bot.message_handler(commands=['file'])
def send_welcome(message):
    doc = open('itmo-table.csv', 'rb')
    bot.send_document(message.chat.id, doc)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


bot.infinity_polling()