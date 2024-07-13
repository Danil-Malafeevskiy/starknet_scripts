import time
from ethereum_gasprice import GaspriceController, GaspriceStrategy
from ethereum_gasprice.providers import EtherscanProvider
from utils.Logger import Logging

class GweiChecker:
    def __init__(self, gwei_limit: int, ETHERSCAN_API_KEY: str, GweiLimitSleep: int, logger: Logging) -> None:
        self.gwei_limit = gwei_limit
        self.controller = GaspriceController(settings={EtherscanProvider.title: ETHERSCAN_API_KEY})
        self.gwei_limit_sleep = GweiLimitSleep
        self.logger = logger 

    def check_gwei(self) -> bool:
        while True:
            try:
                gasprice = self.controller.get_gasprice_by_strategy(GaspriceStrategy.FAST)/int(1e9)
                if gasprice <= self.gwei_limit:
                    return True
                self.logger.log_to_console(f"Gwei сейчас: {gasprice}. Ожидание снижения gwei!", 'error')
                time.sleep(self.gwei_limit_sleep)
            except Exception:
                time.sleep(self.gwei_limit_sleep)
