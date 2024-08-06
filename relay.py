import requests
import random
from core.eth import Web3Client


class Relay(Web3Client):
    def __init__(self, client, logger, settings, config):
        super().__init__(client=client, network=client.network_from, logger=logger, config=config)
        self.client = client
        self.settings = settings
        self.data = None
        self.value = None
        self.to = None
        self.total_fee = None
        self.symbol = None
        self.currency_in = None
        self.currency_out = None
        self.currency_out_usd = None
        self.currency_in_usd = None

    def pre_bridge(self):
        enabled, fee = self.check_enabled_bridge()
        self.logger.info(f'Debank: https://debank.com/profile/{self.address}/history 📃')

        if enabled:
            build_data = self.gather_data()

            self.logger.info(f'[{self.address}] | Make bridge {self.currency_in[:7]} {self.symbol}({self.currency_in_usd}$) | fee: {self.total_fee[:7]}$ 🚀')
        else:
            assert Exception(f'[{self.address}] | The exchange cannot be executed')

        if (int(self.web3.to_wei(self.config.if_the_minimum_account_balance_is_more_than, 'ether')) >
                int(self.web3.eth.get_balance(self.web3.to_checksum_address(self.address)))):
            raise Exception(f'[{self.address}] | Small balance')


    def check_enabled_bridge(self):
        response = requests.get(
            url=f'https://api.relay.link/config/v2?originChainId={self.client.network_from.chain_id}&destinationChainId={self.client.network_to.chain_id}&currency=eth&user=0x0000000000000000000000000000000000000000').json()
        return response["enabled"], response["fee"]

    def gather_data(self):
        json_data = {
            'user': self.get_address_from_private_key(private_key=self.client.private_key),
            'originChainId': self.client.network_from.chain_id,
            'originCurrency': self.settings.token,
            'destinationChainId': self.client.network_to.chain_id,
            'destinationCurrency': self.settings.token,
            'tradeType': 'EXACT_OUTPUT',
            'recipient': self.get_address_from_private_key(private_key=self.client.private_key),
            'amount': int(self.get_balance()
                          *
                          (random.randint(self.settings.amount_percentage[0],
                                          self.settings.amount_percentage[1]) / 100)),
            'usePermit': False,
            'useExternalLiquidity': False,
            'source': 'relay.link/bridge',
        }

        response = requests.post('https://api.relay.link/execute/swap', json=json_data).json()
        self.data = response["steps"][0]["items"][0]["data"]["data"]
        self.value = response["steps"][0]["items"][0]["data"]["value"]
        self.to = response["steps"][0]["items"][0]["data"]["to"]
        self.total_fee = str(
                float(response["fees"]["gas"]["amountUsd"]) +
                float(response["fees"]["relayer"]["amountUsd"]) +
                float(response["fees"]["relayerGas"]["amountUsd"]) +
                float(response["fees"]["relayerService"]["amountUsd"]) +
                float(response["fees"]["app"]["amountUsd"]))
        self.symbol = response["fees"]["gas"]["currency"]["symbol"]
        self.currency_in = response["details"]["currencyIn"]["amountFormatted"]
        self.currency_out = response["details"]["currencyOut"]["amountFormatted"]
        self.currency_in_usd = response["details"]["currencyIn"]["amountUsd"]
        self.currency_out_usd = response["details"]["currencyOut"]["amountUsd"]

        return response

    def bridge(self):
        transaction = self.prepare_transaction(value=int(self.value))
        transaction['data'] = self.data
        transaction['to'] = self.web3.to_checksum_address(self.to)

        submitted_transaction = self.transaction_runner(transaction=transaction)
        if submitted_transaction:
            self.logger.success(f'[{self.address}] | {self.network.explorer}tx/{submitted_transaction.hex()} Bridge success ✅')
