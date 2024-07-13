import json

TOKENS = {
    "DAI": 0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3, 
    "ETH": 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7,
    "USDC": 0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8,
    "USDT": 0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8,
    "wBTC": 0x03fe2b97c1fd336e750087d68b9b867997fd64a2661ff3ca5a7c771641e8e7ac
}

ZK_LEND_ADDR = 0x04c0a5193d58f74fbace4b74dcf65481e734ed1714121bdc571da345540efa05

DMAIL_ADDR = 0x0454f0bd015e730e5adbb4f080b075fdbf55654ff41ee336203aa2e1ac4d4309

STARKVERSE_ADDR = 0x060582df2cd4ad2c988b11fdede5c43f56a432e895df255ccd1af129160044b8

STARKID_ADDR = 0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af

SITHSWAP_ADDR = 0x28c858a586fa12123a1ccb337a0a3b369281f91ea00544d0c086524b759f627

JEDISWAP_ADDR = 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023

PROTOSSSWAP_ADDR = 0x07a0922657e550ba1ef76531454cb6d203d4d168153a0f05671492982c2f7741

TEN_10_KSWAP_ADDR = 0x07a6f98c03379b9513ca84cca1373ff452a7462a3b61598f0af5bb27ad7f76d1

MYSWAP_ADDR = 0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28

AVNU_ADDR = 0x04270219d365d6b017231b52e92b3fb5d7c8378b05e9abc97724537a80e93b0f

UNFRAMED_ADDR = 0x051734077ba7baf5765896c56ce10b389d80cdcee8622e23c0556fb49e82df1b

TASKS_INDEX = {
    "ZkLend": 0,
    "Stark_id": 1,
    "Dmail": 2,
    "StarkVerse": 3,
    "Unframed": 4,
    "DEX": 5
}

with open("data/abi/abi_tokens.json", 'r') as file:
        ABI_TOKENS = json.load(file)

with open("data/abi/abi_unframed.json", 'r') as file:
        ABI_UNFRAMED = json.load(file)

with open("data/abi/abi_dmail.json", 'r') as file:
        ABI_DMAIL = json.load(file)

with open('data/abi/argent.json') as file:
    ARGENT_ABI = json.load(file)

with open('data/abi/abi_zklend.json') as file:
    ABI_ZKLEND = json.load(file)

with open('data/abi/abi_10kswap.json') as file:
    ABI_TENKSWAP = json.load(file)

with open('data/abi/abi_jediswap.json') as file:
    ABI_JEDISWAP = json.load(file)

with open('data/abi/abi_myswap.json') as file:
    ABI_MYSWAP = json.load(file)

with open('data/abi/abi_sithswap.json') as file:
    ABI_SITHSWAP = json.load(file)

with open('data/abi/abi_starkid.json') as file:
    ABI_STARKID = json.load(file)

with open('data/abi/abi_starkverse.json') as file:
    ABI_STARKVERSE = json.load(file)

with open('data/abi/abi_avnu.json') as file:
    ABI_AVNU = json.load(file)

with open("data/config.json", 'r') as file:
    CONFIG = json.load(file)

with open("data/addresses.txt", 'r') as file:
    ADDRESSES = [line.rstrip() for line in file]


ARGENT_INIT_CLASS_HASH = 0x025EC026985A3BF9D0CC1FE17326B245DFDC3FF89B8FDE106542A3EA56C5A918

ARGENT_INVOKATION_CLASS_HASH = 0x33434AD846CDD5F23EB73FF09FE6FDDD568284A0FB7D1BE20EE482F044DABE2

ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW = 0x01a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003