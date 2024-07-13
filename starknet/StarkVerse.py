from starknet_py.contract import Contract
from starknet.starknet import StarkNet
import asyncio
from starknet_py.net.account.account import Account
from utils.Logger import Logging
from utils.GweiChecker import GweiChecker
from starknet.constants import STARKVERSE_ADDR, ABI_STARKVERSE

class StarkVerse(StarkNet):

    def __init__(self, 
                 account: Account, 
                 logger: Logging,  
                 gwei_checker: GweiChecker, 
                 ErrorRetry: int, 
                 ErrorSleep: int) -> None:
        
        super().__init__(account, logger, gwei_checker, ErrorRetry, ErrorSleep, 
                         Contract(address=STARKVERSE_ADDR, provider=account, abi=ABI_STARKVERSE),
                         "StarkVerse",
                         "publicMint")

    def random_args(self) -> list:
        return [self.account.address]