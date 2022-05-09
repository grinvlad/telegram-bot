import random
import requests
from collections import deque


class MemeQue:
    meme_que: deque[str] | None = None

    def __init__(self):
        if not type(self).meme_que:
            type(self)._make_random_queue()

    @classmethod
    def _make_random_queue(cls) -> None:
        with open('utils/memes.txt', 'r') as meme_file:
            memes = meme_file.read().strip(' \n').split('\n')
        cls.meme_que = deque(random.sample(memes, len(memes)))

    @classmethod
    def get_next_meme(cls) -> str:
        return cls.meme_que.popleft()

    @classmethod
    def add_new_meme(cls, url: str) -> int:
        cls.meme_que.append(url)
        with open('utils/memes.txt', 'a') as meme_file:
            meme_file.write('\n' + url)
        return len(cls.meme_que)

    @classmethod
    def illegally_add_new_meme(cls, url: str) -> int:
        cls.meme_que.appendleft(url)
        return 1

    @classmethod
    def __len__(cls) -> int:
        return len(cls.meme_que)


def when_to_send_meme(message) -> bool:
    triggers = ('а сейчас, несмешной мем от тани',
                'а сейчас, смешной мем от тани',
                'несмешной мем от тани',
                'смешной мем от тани',
                'мем от тани',
                'кринж от тани',
                'мем',
                'еще мем',
                'чтобы прям смешно',
                'чтобы все уссались')
    return message.text.lower() in triggers


def when_to_add_new_meme(message) -> bool:
    potential_url = message if isinstance(message, str) else message.text
    if not potential_url.startswith('http'):
        return False
    try:
        response = requests.get(potential_url)
    except requests.exceptions.RequestException:
        return False
    if response.headers['Content-Type'].startswith('image/'):
        return True
    return False


def when_to_illegally_add_new_meme(message) -> bool:
    try:
        option, potential_url = message.text.split(maxsplit=1)
    except ValueError:
        return False
    return option == '-i' and when_to_add_new_meme(potential_url)
