import random
from loguru import logger
from sys import stderr
import time


def wallet_reader(shuffle):
    with open('data/wallets.txt') as file:
        if shuffle:
            accounts = [i.strip() for i in file]
            random.shuffle(accounts)
            return accounts, len(accounts)
        else:
            return [i.strip() for i in file], len([i.strip() for i in file])


def add_logger():
    logger.remove()
    logger.add(
        stderr, diagnose=True,
        format="<bold><blue>{time:HH:mm:ss}</blue> | <level>{level: <8}</level> | <level>{message}</level></bold>"
    )
    logger.add(sink='./log/logfile.log', rotation="50 MB")
    return logger


def sleep_module(config):
    logger.debug(f'💤 sleep')
    time.sleep(random.randint(config.sleep[0], config.sleep[1]))


def interface(_len, network_from, network_to, config):
    print(
        f"""\033[36m   Developed by @Irorsss \033[m\033[96m
        
Total wallets loaded: {_len}
Bridge: {network_from} ---> {network_to}
Maximum code execution time: {int(_len * config.sleep[1] / 60)} min
\033[m """
    )

    print()
    time.sleep(3)
