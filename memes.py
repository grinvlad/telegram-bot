from random import randrange


class Meme:
    with open('utils/memes.txt', 'r') as meme_file:
        _memes = meme_file.read().split('\n')
    n = len(_memes)

    @staticmethod
    def get_random_url():
        return Meme._memes[randrange(Meme.n)]

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
