from starknet_py.contract import Contract
from starknet.starknet import StarkNet
import random
from starknet_py.net.account.account import Account
from utils.Logger import Logging
from utils.GweiChecker import GweiChecker
from starknet.constants import TOKENS

class Swap(StarkNet):

    def __init__(self, 
                 account: Account, 
                 logger: Logging, 
                 gwei_checker: GweiChecker, 
                 ErrorRetry: int, 
                 ErrorSleep: int, 
                 contract: Contract,
                 task_name: str,
                 invoke_function: str,
                 WorkPercentSwapETH: list,
                 SaveEthOnBalance: list,
                 toSaveFunds: str) -> None:
    
        super().__init__(account, logger, gwei_checker, ErrorRetry, ErrorSleep,
                         contract,
                         task_name,
                         invoke_function)
        self.tokens = TOKENS
        self.WorkPercentSwapETH = WorkPercentSwapETH
        self.SaveEthOnBalance = SaveEthOnBalance
        self.toSaveFunds = toSaveFunds

    def random_args(self, from_token: str, to_token: str) -> list:
        return [self.tokens[from_token], self.tokens[to_token],
                random.uniform(self.SaveEthOnBalance[0], self.SaveEthOnBalance[1]) if from_token == "ETH" else 0,
                random.randint(int(self.WorkPercentSwapETH[0]*100), int(self.WorkPercentSwapETH[1]*100)) if from_token == "ETH" else 100]

    def swap(self, args: list) -> (bool, int):
        calls = args
        return self.transaction(calls, self.task_name)

    def start_task(self, from_token: int, to_token: int) -> (bool, int):
        args = self.random_args(from_token, to_token)
        return self.swap(args)