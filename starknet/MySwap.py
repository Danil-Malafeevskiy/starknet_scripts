from starknet_py.contract import Contract
import asyncio
from starknet_py.net.account.account import Account
from utils.Logger import Logging
from utils.GweiChecker import GweiChecker
from starknet.constants import MYSWAP_ADDR, ABI_TOKENS, ABI_MYSWAP
from starknet.Swap import Swap

class MySwap(Swap):

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
                         Contract(address=MYSWAP_ADDR, provider=account, abi=ABI_MYSWAP),
                         'MySwap',
                         "", WorkPercentSwapETH, SaveEthOnBalance, toSaveFunds)


    def get_pool_id(self, from_token: int):
        pool_id = 1
        reverse = False

        if self.tokens["USDC"] == from_token:
            reverse = True

        return pool_id, reverse
    

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

        path = [args[0], args[1]]

        pool_id, reverse = self.get_pool_id(args[0])

        get_pool_data = self.contract.functions["get_pool"].prepare(pool_id)
        (pool_data, ), retryLimit = self.get_other_args(get_pool_data)

        if retryLimit == 0:
            return (True, retryLimit)

        if reverse:
            reserveIn = pool_data.get("token_b_reserves")
            reserveOut = pool_data.get("token_a_reserves")
        else:
            reserveIn = pool_data.get("token_a_reserves")
            reserveOut = pool_data.get("token_b_reserves")

        min_amount_out = reserveOut * amount_wei / reserveIn
        min_amount_out = int(min_amount_out - (min_amount_out / 100))
        
        calls = [
            approve_token_contract.functions["approve"].prepare(self.contract.address, amount_wei),
            self.contract.functions["swap"].prepare(pool_id, args[0], amount_wei, min_amount_out)
        ]

        return self.transaction(calls, self.task_name)