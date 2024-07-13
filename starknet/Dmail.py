from starknet_py.contract import Contract
from starknet.starknet import StarkNet
import asyncio
import random
from starknet_py.net.account.account import Account
from utils.Logger import Logging
from utils.GweiChecker import GweiChecker
from starknet.constants import DMAIL_ADDR, ABI_DMAIL

class Dmail(StarkNet):

    def __init__(self, 
                 account: Account, 
                 logger: Logging, 
                 gwei_checker: GweiChecker, 
                 ErrorRetry: int, 
                 ErrorSleep: int) -> None:
        
        super().__init__(account, logger, gwei_checker, ErrorRetry, ErrorSleep,
                         Contract(address=DMAIL_ADDR, provider=account, abi=ABI_DMAIL),
                         'Dmail',
                         "transaction")

    def random_args(self) -> list:
        domain_list = ["@gmail.com", "@dmail.ai"]

        domain_address = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(5, 10)))
        theme = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(10, 20)))

        return [domain_address + random.choice(domain_list), theme]