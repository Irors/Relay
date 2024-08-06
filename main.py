from core.other import wallet_reader, add_logger, sleep_module, interface
from data.settings import Config, RelayBridgeSettings
from relay import Relay


class Client:
    def __init__(self, private_key, network_from, network_to, _logger):
        self.private_key = private_key
        self.network_from = network_from
        self.network_to = network_to
        self.settings = RelayBridgeSettings()
        self.config = Config()
        self.logger = _logger


def set_up():
    return RelayBridgeSettings(), Config(), add_logger()


def start_module(_client):
    relay = Relay(client=_client, logger=client.logger, settings=client.settings, config=_client.config)
    relay.pre_bridge()
    relay.bridge()


if __name__ == "__main__":
    pre_settings, pre_config, logger = set_up()
    accounts, _len = wallet_reader(shuffle=pre_config.shuffle_wallet)
    interface(_len, pre_settings.network_from, pre_settings.network_to, config=pre_config)

    clients = [Client(private_key=private_key,
                      network_from=pre_settings.network_from,
                      network_to=pre_settings.network_to,
                      _logger=logger) for private_key in accounts]

    for client in clients:
        try:
            start_module(_client=client)
            sleep_module(config=pre_config)

            with open(rf'data\result\success.txt', 'a+') as file:
                datas = [i.strip() for i in file]
                if datas.count(client.private_key) == 0:
                    file.write(f'{client.private_key}\n')

        except Exception as err:
            logger.error(err)

            with open(rf'data\result\failure.txt', 'a+') as file:
                datas = [i.strip() for i in file]
                if datas.count(client.private_key) == 0:
                    file.write(f'{client.private_key}\n')