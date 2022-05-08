import random
from random import randrange


class Meme:
    meme_queue: list[str] | None = None

    def __init__(self):
        if not type(self).meme_queue:
            type(self)._make_random_queue()

    @classmethod
    def _make_random_queue(cls):
        with open('utils/memes.txt', 'r') as meme_file:
            memes = meme_file.read().split('\n')
        cls.meme_queue = random.sample(memes, len(memes))

    @classmethod
    def get_random_url(cls):
        return cls.meme_queue.pop()

    @staticmethod
    def when_to_send_meme(message):
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
