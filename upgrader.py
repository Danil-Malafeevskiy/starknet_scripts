import random
from threading import Thread
import time
from starknet.constants import CONFIG, ADDRESSES
from starknet.starknet import StarkNet
from utils.GweiChecker import GweiChecker
from utils.Logger import Logging
from utils.utils import get_accounts, get_priv_keys


config = CONFIG
addresses = ADDRESSES
priv_keys = get_priv_keys()
logger = Logging()

ErrorSleep = config['ErrorDelayTime']
Retries = config['RetriesLimit']
gwei_limit = config['gwei_limit']
ETHERSCAN_API_KEY = config["ETHERSCAN_API_KEY"]
GweiLimitSleep = config['GweiLimitSleep']
startsleeptime = config["startsleeptime"]
ThreadAccountSleep = config['ThreadAccountSleep']

gwei_cheker = GweiChecker(gwei_limit, ETHERSCAN_API_KEY, GweiLimitSleep, logger)

thread_list = []

accounts = get_accounts(priv_keys, addresses)

logger.log_to_console(f"Ожидание старта запуска скрипта - {startsleeptime}сек...", 'info')
time.sleep(startsleeptime)

for acc in accounts:
    logger.log_to_console(f"Начало апгрейда адреса - {hex(acc.address)}", 'info')
    th = Thread(target=StarkNet.upgrade_wallet, args=(acc, logger, gwei_cheker, Retries, ErrorSleep))
    thread_list.append(th)
    th.start()
    time.sleep(random.randint(ThreadAccountSleep[0], ThreadAccountSleep[1]))