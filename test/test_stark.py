import random
from starknet_py.contract import Contract
from starknet_py.net.account.account import Account
from starknet_py.hash.address import compute_address
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.gateway_client import GatewayClient
import asyncio
import json
import time
from threading import Thread
import string 
from starknet_py.transaction_errors import TransactionFailedError
from starknet_py.net.client_errors import ClientError
from starknet_py.net.client_models import Call
from starknet_py.hash.selector import get_selector_from_name

print(0x07ae7ba4174f6b5c09e05acda13c9adddabeecafe92077e7f2dfaf86becda866)

'''key_pair = KeyPair.from_private_key(3235719860702926964985752763691965749491321155525252832126671737574328281032)

selector = get_selector_from_name("initialize")

calldata = [key_pair.public_key, 0]

address = compute_address(
    class_hash=0x025EC026985A3BF9D0CC1FE17326B245DFDC3FF89B8FDE106542A3EA56C5A918,
    constructor_calldata=[0x33434AD846CDD5F23EB73FF09FE6FDDD568284A0FB7D1BE20EE482F044DABE2, selector, len(calldata), *calldata],
    salt=key_pair.public_key,
)

print(hex(address))'''