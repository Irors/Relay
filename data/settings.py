from .network import *


class Config:
    sleep = [22, 66]
    gas_price_multiplier = 5
    gas_limit_multiplier = 5
    shuffle_wallet = True
    if_the_minimum_account_balance_is_more_than = 0.001  # Если баланс аккаунта меньше указанного числа, то вывод средств выполнятся не будет


class RelayBridgeSettings:
    """
    Chain
    тут перечислены только часто используемые сети
    Chain #42161 Arbitrum

    Chain #42170 Arbitrum Nova

    Chain #8453 Base

    Chain #81457 Blast

    Chain #1 Ethereum

    Chain #59144 Linea

    Chain #10 Optimism

    Chain #534352 Scroll

    Chain #324 zkSync Era
    """

    network_from = ScrollRPC
    network_to = BaseRPC

    token = '0x0000000000000000000000000000000000000000'  # native

    amount_percentage = [85, 94]
