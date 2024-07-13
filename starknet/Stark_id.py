from starknet_py.contract import Contract
from starknet.starknet import StarkNet
import asyncio
import random
from starknet_py.net.account.account import Account
from utils.Logger import Logging
from utils.GweiChecker import GweiChecker
from starknet.constants import STARKID_ADDR, ABI_STARKID

class StarkId(StarkNet):

    def __init__(self, 
                 account: Account, 
                 logger: Logging, 
                 gwei_checker: GweiChecker, 
                 ErrorRetry: int, 
                 ErrorSleep: int) -> None:
        
        super().__init__(account, logger, gwei_checker, ErrorRetry, ErrorSleep,
                         Contract(address=STARKID_ADDR, provider=account, abi=ABI_STARKID),
                         'starkid',
                         "mint")

    def random_args(self) -> list:
        return [random.randint(100000000000, 999999999999)]