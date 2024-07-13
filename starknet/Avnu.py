import requests
from starknet_py.contract import Contract
import asyncio
from starknet_py.net.account.account import Account
from utils.Logger import Logging
from utils.GweiChecker import GweiChecker
from starknet.constants import AVNU_ADDR, ABI_TOKENS, ABI_AVNU
from starknet.Swap import Swap
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call

class Avnu(Swap):

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
                         Contract(address=AVNU_ADDR, provider=account, abi=ABI_AVNU),
                         'Avnu',
                         "", WorkPercentSwapETH, SaveEthOnBalance, toSaveFunds)

    def get_quotes(self,from_token: int, to_token: int, amount: int):
        url = "https://starknet.api.avnu.fi/swap/v1/quotes"

        params = {
            "sellTokenAddress": hex(from_token),
            "buyTokenAddress": hex(to_token),
            "sellAmount": hex(amount),
            "excludeSources": "Ekubo"
        }

        response = requests.get(url=url, params=params)
        response_data = response.json()

        quote_id = response_data[0]["quoteId"]

        return quote_id
        

    def build_transaction(self, quote_id: str, recipient: int):
        url = "https://starknet.api.avnu.fi/swap/v1/build"

        data = {
            "quoteId": quote_id,
            "takerAddress": hex(recipient),
            "slippage": float(1 / 100),
        }

        response = requests.post(url=url, json=data)
        response_data = response.json()

        return response_data


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

        quote_id = self.get_quotes(args[0], args[1], amount_wei)

        transaction_data = self.build_transaction(quote_id, self.account.address)

        calldata = [int(i, 16) for i in transaction_data["calldata"]]
        
        calls = [
            approve_token_contract.functions["approve"].prepare(self.contract.address, amount_wei),
            Call(to_addr=self.contract.address, selector=get_selector_from_name(transaction_data["entrypoint"]), calldata=calldata)
        ]

        return self.transaction(calls, self.task_name)