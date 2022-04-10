import logging
import functools

logging.basicConfig(format='%(levelname)s | %(asctime)s | %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='utils/bot.log',
                    encoding='utf-8',
                    level=logging.INFO)


def log(func):
    @functools.wraps(func)
    def wrapper(message):
        logging.info(f'-> {func.__name__}() | {message.from_user.username} | {message.text}')
        result = func(message)
        logging.info(f'<- {func.__name__}() | {message.from_user.username}')
        return result
    return wrapper
