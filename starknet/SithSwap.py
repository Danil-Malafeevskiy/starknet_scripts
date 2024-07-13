import time
from starknet_py.contract import Contract
import asyncio
from starknet_py.net.account.account import Account
from utils.Logger import Logging
from utils.GweiChecker import GweiChecker
from starknet.constants import SITHSWAP_ADDR, ABI_TOKENS, ABI_SITHSWAP
from starknet.Swap import Swap

class SithSwap(Swap):

    def __init__(self, 
                 account: Account, 
                 logger: Logging, 
                 gwei_checker: GweiChecker, 
                 ErrorRetry: int, 
                 ErrorSleep: int, 
                 WorkPercentSwapETH: list,
                 SaveEthOnBalance: list,
                 toSaveFunds: str) -> None:
    
        super().__init__(account, logger, gwei_checker, ErrorRetry, ErrorSleep,
                         Contract(address=SITHSWAP_ADDR, provider=account, abi=ABI_SITHSWAP),
                         'SithSwap',
                         "", WorkPercentSwapETH, SaveEthOnBalance, toSaveFunds)

    def swap(self, args: list) -> (bool, int):
        proxy_config = True
        abi = None
        if self.tokens['USDC'] == args[0]:
            proxy_config = False
            abi = ABI_TOKENS

        approve_token_contract = self.get_contract(args[0], abi, proxy_config)

        amount_wei, amount, balance, retryLimit, retryLimit_2 = self.get_amount(args[0], args[3])

        if retryLimit == 0 or retryLimit_2 == 0:
            return (True, 0)

        if amount_wei < args[2]:
            return (False, 1)

        get_min_amount_out_data = self.contract.functions["getAmountOut"].prepare(amount_wei, args[0], args[1])
        min_amount_out_data, retryLimit = self.get_other_args(get_min_amount_out_data)

        if retryLimit == 0:
            return (True, retryLimit)

        min_amount_out = int(min_amount_out_data.amount - (min_amount_out_data.amount / 100 ))
        stable = min_amount_out_data.stable

        deadline = int(time.time()) + 1000000
        route = [{"from_address": args[0], "to_address": args[1], "stable": stable}]

        calls = [
            approve_token_contract.functions["approve"].prepare(self.contract.address, amount_wei),
            self.contract.functions["swapExactTokensForTokensSupportingFeeOnTransferTokens"].prepare(amount_wei, min_amount_out, route, self.account.address, deadline)
        ]

        return self.transaction(calls, self.task_name)