from starknet_py.contract import Contract
from starknet.starknet import StarkNet
import asyncio
import random
from starknet_py.net.account.account import Account
from utils.Logger import Logging
from utils.GweiChecker import GweiChecker
from starknet.constants import TOKENS, ZK_LEND_ADDR, ABI_ZKLEND

class ZkLend(StarkNet):

    def __init__(self, 
                 account: Account, 
                 logger: Logging, 
                 gwei_checker: GweiChecker, 
                 ErrorRetry: int, 
                 ErrorSleep: int) -> None:
        
        super().__init__(account, logger, gwei_checker, ErrorRetry, ErrorSleep,
                         Contract(address=ZK_LEND_ADDR, provider=account, abi=ABI_ZKLEND),
                         'ZkLend',
                         "")
        self.tokens = TOKENS
        self.invoke_functions = ["enable_collateral", "disable_collateral"]
        self.call_function = "is_collateral_enabled"

    def random_args(self) -> list:
        return [random.choice(list(self.tokens.values()))]


    def start_task(self) -> (bool, int):
        args = self.random_args()

        is_collateral_check = self.contract.functions[self.call_function].prepare(self.account.address, *args)
        is_collateral, retryLimit = self.get_other_args(is_collateral_check)
        
        if  retryLimit == 0:
            return (True, retryLimit)

        calls = [
            self.contract.functions[self.invoke_functions[is_collateral[0]]].prepare(*args)
        ]

        return self.transaction(calls, self.task_name)