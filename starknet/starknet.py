import asyncio
import random
import time
from starknet_py.net.account.account import Account
from starknet_py.transaction_errors import TransactionFailedError
from starknet_py.net.client_errors import ClientError
from web3 import Web3
from utils.Logger import Logging
from utils.GweiChecker import GweiChecker
from starknet_py.contract import Contract, PreparedFunctionCall
from starknet.constants import ABI_TOKENS, TOKENS, ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW, ARGENT_ABI

class StarkNet:
    
    def __init__(self, 
                 account: Account, 
                 logger: Logging, 
                 gwei_checker: GweiChecker, 
                 ErrorRetry: int, 
                 ErrorSleep: int,
                 contract: Contract,
                 task_name: str,
                 invoke_function: str) -> None:
        
        self.account = account
        self.logger = logger
        self.gwei_checker = gwei_checker
        self.ErrorRetry = ErrorRetry
        self.ErrorSleep = ErrorSleep
        self.contract = contract
        self.task_name = task_name
        self.invoke_function = invoke_function
        
    @staticmethod
    def generate_tasks_count(Tasks: dict) -> (list, int, dict):
        len_tasks = 0
        tasks = []
        for key, value in Tasks.items():
            count_task = random.randint(value[0], value[1])
            tasks += [key]*count_task
            len_tasks += count_task
            Tasks[key] = count_task
        return tasks, len_tasks, Tasks

    def transaction(self, calls: list, task_name: str) -> (bool, int):
        retryLimit = self.ErrorRetry 
        balance = True
        while retryLimit:
            try: 
                self.gwei_checker.check_gwei()

                self.logger.log_to_console(f"Адрес: {hex(self.account.address)} - выполняет задание: {task_name}", 'info')

                invocation = asyncio.run(self.account.execute(calls=calls, auto_estimate=True, nonce=asyncio.run(self.account.get_nonce())))
  
                asyncio.run(self.account.client.wait_for_tx(invocation.transaction_hash))
                
                break
            except (ClientError, TransactionFailedError) as e:
                if e.message.find('INSUFFICIENT_ACCOUNT_BALANCE') != -1:
                    balance = False
                    return balance, retryLimit

                self.logger.log_to_console(f"Адрес: {hex(self.account.address)} - не смог выполнить задание: {task_name}. Повторная попытка через {self.ErrorSleep}", 'error')

                time.sleep(self.ErrorSleep)
                retryLimit -= 1

        return balance, retryLimit
    

    def get_other_args(self, prep_func: PreparedFunctionCall):
        retryLimit = self.ErrorRetry
        while retryLimit:
            try:
                resp = asyncio.run(prep_func.call())
                break
            except ClientError:
                time.sleep(self.ErrorSleep)
                retryLimit -= 1
        
        return resp, retryLimit
    

    def random_args() -> list:
        return []


    def start_task(self) -> (bool, int):
        args = self.random_args()
        
        calls = [
            self.contract.functions[self.invoke_function].prepare(*args)
        ]

        return self.transaction(calls, self.task_name)
    

    def get_contract(self, address: int, abi: dict = None, proxy_config: bool = False) -> Contract:
        if abi != None:
            return Contract(address=address, provider=self.account, abi=abi)
        
        return asyncio.run(Contract.from_address(address=address, provider=self.account, proxy_config=proxy_config))


    def get_balance_stable_coin(self, contract_address: int) -> (dict, int, int):
        contract = self.get_contract(contract_address, abi=ABI_TOKENS)

        decimal, retryLimit = self.get_other_args(contract.functions["decimals"].prepare())

        balance_wei, retryLimit_2 = self.get_other_args(contract.functions["balanceOf"].prepare(self.account.address))

        balance = balance_wei.balance / 10 ** decimal.decimals

        return {"balance_wei": balance_wei.balance, "balance": balance, "decimal": decimal.decimals}, retryLimit, retryLimit_2
    
    def get_amount(self, from_token: int, random_percent: int):
        retryLimit, retryLimit_2 = 1, 1 
        if TOKENS['ETH'] == from_token:
            balance = asyncio.run(self.account.get_balance())
            amount_wei = int(balance / 100 * random_percent)
            amount = Web3.from_wei(int(balance / 100 * random_percent), "ether")
        else:
            balance, retryLimit, retryLimit_2 = self.get_balance_stable_coin(from_token)
            amount_wei = int(balance["balance_wei"] / 100 * random_percent)
            amount = balance["balance"] / 100 * random_percent
            balance = balance["balance_wei"]

        return amount_wei, amount, balance, retryLimit, retryLimit_2


    @staticmethod
    def upgrade_wallet(acc: Account, logger: Logging, gwei_checker: GweiChecker, retryLimit: int, ErrorSleep: int):
        class_hash = ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW

        while retryLimit:
            try: 
                contract = Contract(address=acc.address, provider=acc, abi=ARGENT_ABI)

                account_version = asyncio.run(contract.functions["getVersion"].call())

                version = bytes.fromhex(hex(account_version.as_tuple()[0])[2:]).decode("utf8")

                if version == "0.2.3":
                    logger.log_to_console(f"{hex(acc.address)} - Upgrade account to cairo 1", 'info')

                    gwei_checker.check_gwei()

                    upgrade_call = [contract.functions["upgrade"].prepare(class_hash, [0])]

                    invocation = asyncio.run(acc.execute(calls=upgrade_call, auto_estimate=True))
    
                    res = asyncio.run(acc.client.wait_for_tx(invocation.transaction_hash))

                    if res.status.value not in ['ACCEPTED_ON_L2', 'ACCEPTED_ON_L1', 'SUCCEEDED']:
                        raise TransactionFailedError("Transaction NOT Accepted!")

                else:
                    logger.log_to_console(f"{hex(acc.address)} - No upgrade required", 'info')
                
                logger.log_to_console(f"{hex(acc.address)} - Upgraded account to cairo 1", 'info')

                break

            except (ClientError, TransactionFailedError) as e:
                if e.message.find('INSUFFICIENT_ACCOUNT_BALANCE') != -1:
                    logger.log_to_console(f"На адресе: {hex(acc.address)} - закончились деньги. Перехожу к следующему апгрейду!", 'error')
                    break

                logger.log_to_console(f"Адрес: {hex(acc.address)} - не смог произвести upgrade. Повторная попытка через {ErrorSleep}", 'error')

                time.sleep(ErrorSleep)
                retryLimit -= 1