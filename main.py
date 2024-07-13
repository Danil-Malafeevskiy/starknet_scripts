import random
from starknet_py.net.account.account import Account
import time
from threading import Thread
from utils.Logger import Logging
from utils.GweiChecker import GweiChecker
from starknet.starknet import StarkNet
from starknet.constants import TASKS_INDEX, CONFIG, ADDRESSES
from utils.utils import get_priv_keys, get_accounts, tasks_interface, swap

def main(account: Account, Tasks: dict, task_sleep: list, ErrorSleep: int, ErrorRetry: int, gwei_cheker: GweiChecker,
                 logger: Logging, WorkPercentSwapETH: list, toSaveFunds: str, SaveEthOnBalance: list) -> None: 
    
    tasks, len_tasks, Tasks = StarkNet.generate_tasks_count(Tasks)
    logger.log_to_console(f"Список заданий для кошелька {hex(account.address)}: {Tasks}", 'info')
    
    balance = True

    tasks_obj = tasks_interface([account, logger, gwei_cheker, ErrorRetry, ErrorSleep], [WorkPercentSwapETH, SaveEthOnBalance, toSaveFunds])

    for task_name in random.sample(tasks, len_tasks):
        
        task_obj = tasks_obj[TASKS_INDEX[task_name]]
        if task_name == "DEX":
            balance, retryLimit = swap(task_obj, toSaveFunds, task_sleep)
        else:
            balance, retryLimit = task_obj.start_task()

        if balance == False: 
            logger.log_to_console(f"На адресе: {hex(account.address)} - закончился баланс...", 'error')
            break
        
        elif retryLimit == 0: 
            logger.log_to_console(f"Адрес: {hex(account.address)} - сделал максимально число попыток выполнения задания неудачно, переход к следующему заданию...", 'error')
            continue
        
        logger.log_to_console(f"Адрес: {hex(account.address)} - успешно выполнил задание: {task_name}.", 'info')

        time.sleep(random.randint(task_sleep[0], task_sleep[1]))
    
    logger.log_to_console(f"Адрес: {hex(account.address)} - завершает работу...", 'info')


if __name__ == "__main__":
    logger = Logging()

    cairo_version = int(input("Введите cairo-версию кошельков (default 0): ") or 0)
    
    logger.log_to_console("Обработка ардесов и файла конфига и получение аккаунтов...", 'info')
    priv_key = get_priv_keys()
    addresses = ADDRESSES
    config = CONFIG

    accounts = get_accounts(priv_key, addresses, cairo_version)
    accounts_count = len(accounts)
    accounts = random.sample(accounts, accounts_count)

    logger.log_to_console(f'Количесво собранных аккаунтов: {accounts_count}', 'info')
    
    TaskSleep = config['TaskSleep']
    ThreadAccountSleep = config['ThreadAccountSleep']
    Tasks = config['Tasks']
    ErrorSleep = config['ErrorDelayTime']
    Retries = config['RetriesLimit']
    gwei_limit = config['gwei_limit']
    ETHERSCAN_API_KEY = config["ETHERSCAN_API_KEY"]
    GweiLimitSleep = config['GweiLimitSleep']
    WorkPercentSwapETH = config['WorkPercentSwapETH']
    toSaveFunds = config["toSaveFunds"]
    SaveEthOnBalance = config["SaveEthOnBalance"]
    startsleeptime = config["startsleeptime"]

    gwei_cheker = GweiChecker(gwei_limit, ETHERSCAN_API_KEY, GweiLimitSleep, logger)
    
    thread_list = []
    acc: Account

    logger.log_to_console(f"Ожидание старта запуска скрипта - {startsleeptime}сек...", 'info')
    time.sleep(startsleeptime)

    for acc in accounts:
        logger.log_to_console(f"Начало работы адреса - {hex(acc.address)}", 'info')
        th = Thread(target=main, args=(acc, dict(Tasks), TaskSleep, ErrorSleep, Retries, gwei_cheker, logger, WorkPercentSwapETH, toSaveFunds, SaveEthOnBalance))
        thread_list.append(th)
        th.start()
        time.sleep(random.randint(ThreadAccountSleep[0], ThreadAccountSleep[1]))

    for th in thread_list:
        th.join()

    logger.log_to_console("Конец работы программы...", 'info')