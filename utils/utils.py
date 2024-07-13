from getpass import getpass
import random
from cryptography.fernet import Fernet
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.full_node_client import FullNodeClient
from starknet.Dmail import Dmail
from starknet.StarkVerse import StarkVerse
from starknet.ZkLend import ZkLend
from starknet.Stark_id import StarkId
from starknet.SithSwap import SithSwap
from starknet.JediSwap import JediSwap
from starknet.tenkswap import TenKSwap
from starknet.MySwap import MySwap
from starknet.Unframed import Unframed
import time
from starknet.constants import ARGENT_INIT_CLASS_HASH, ARGENT_INVOKATION_CLASS_HASH, ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW
from base64 import urlsafe_b64encode
from starknet.Avnu import Avnu
from starknet_py.hash.address import compute_address
from starknet_py.hash.selector import get_selector_from_name

def get_accounts(priv_keys: list, addresses: list, cairo_version: int = 0) -> list:
    accounts = []

    addresses = [int(addr, 16) for addr in addresses]

    for priv_key in priv_keys:
        key_pair = KeyPair.from_private_key(priv_key)

        selector = get_selector_from_name("initialize")

        calldata = [key_pair.public_key, 0]

        if cairo_version == 0:
            address = compute_address(
                    class_hash=ARGENT_INIT_CLASS_HASH,
                    constructor_calldata=[ARGENT_INVOKATION_CLASS_HASH, selector, len(calldata), *calldata],
                    salt=key_pair.public_key
            )
        else:
            address = compute_address(
                    class_hash=ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW,
                    constructor_calldata=calldata,
                    salt=key_pair.public_key,
            )

        if address in addresses:
            account = Account(
                client=FullNodeClient("https://starknet-mainnet.public.blastapi.io"),
                address=address,
                key_pair= KeyPair.from_private_key(key=priv_key),
                chain=StarknetChainId.MAINNET
            )

            accounts.append(account)
    
    return accounts


def get_priv_keys() -> (dict, list, list):
    with open("data/private_key_shiphr.txt", 'r') as file:
        priv_keys = [line.rstrip() for line in file]

    return decrypt(priv_keys)


def decrypt(priv_keys: list) -> list:

    key = urlsafe_b64encode(getpass("Введите пароль для расшифровки 32х символов: ").encode())
    old_keys = []
    for priv_key in priv_keys:
        old_keys.append(Fernet(key).decrypt(priv_key.encode()).decode())

    return old_keys


def tasks_interface(shared_args: list, swap_args: list) -> list:
    dmail = Dmail(*shared_args)
    zklend = ZkLend(*shared_args)
    starkid = StarkId(*shared_args)
    starkverse = StarkVerse(*shared_args)
    unframed = Unframed(*shared_args)
    dex = [TenKSwap(*shared_args, *swap_args), SithSwap(*shared_args, *swap_args), JediSwap(*shared_args, *swap_args), MySwap(*shared_args, *swap_args), Avnu(*shared_args, *swap_args)]

    return [zklend, starkid, dmail, starkverse, unframed, dex]

def swap(swap_obj: list, toSaveFounds: int, task_sleep: list):
    task_obj = random.choice(swap_obj)
    balance, retryLimit = task_obj.start_task("ETH", "USDC")

    if balance and retryLimit > 0 and toSaveFounds == "ETH":
        time.sleep(random.randint(task_sleep[0], task_sleep[1]))

        task_obj = random.choice(swap_obj)
        balance, retryLimit = task_obj.start_task("USDC", "ETH")

    return balance, retryLimit