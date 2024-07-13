from starknet_py.contract import Contract
from starknet.starknet import StarkNet
import asyncio
import random
from starknet_py.net.account.account import Account
from utils.Logger import Logging
from utils.GweiChecker import GweiChecker
from starknet.constants import UNFRAMED_ADDR, ABI_UNFRAMED

class Unframed(StarkNet):

    def __init__(self, 
                 account: Account, 
                 logger: Logging, 
                 gwei_checker: GweiChecker, 
                 ErrorRetry: int, 
                 ErrorSleep: int) -> None:
        
        super().__init__(account, logger, gwei_checker, ErrorRetry, ErrorSleep,
                         Contract(address=UNFRAMED_ADDR, provider=account, abi=ABI_UNFRAMED, cairo_version=1),
                         'Unframed',
                         "cancel_orders")

    def random_args(self) -> list:
        return [[random.randint(
            296313738189912513306030367211954909183182558840765666364410788857347237284,
            3618502788666131213697322783095070105623107215331596699973092056135872020480)]]