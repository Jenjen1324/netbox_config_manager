from functools import lru_cache

import hvac

from netbox.settings import PLUGINS_CONFIG


class VaultClient:

    def __init__(self):
        config = PLUGINS_CONFIG['netbox_config_manager']

        args = {
            'url': config['vault_url'],
            'token': config['vault_token'],
            'client_cert_path': config['vault_client_cert_path'],
            'server_cert_path': config['vault_server_cert_path'],
            'namespace': config['vault_namespace']
        }

        if not args['client_cert_path']:
            del args['client_cert_path']
        if not args['server_cert_path']:
            del args['server_cert_path']
        if not args['namespace']:
            del args['namespace']

        self.client = hvac.Client(**args)

        self.secrets_path = 'netbox/transport_configuration'

        if not self.client.is_authenticated():
            raise Exception('VaultClient could not authenticate. Please verify configuration')

    def _get_transport_configuration_path(self, secret_reference: str):
        return f'{self.secrets_path}/{secret_reference}'

    def put_transport_configuration_secret(self, secret_reference: str, secret: str):
        self.client.secrets.kv.v2.create_or_update_secret(
            path=self._get_transport_configuration_path(secret_reference),
            secret={'key': secret}
        )

    def get_transport_configuration_secret(self, secret_reference: str):
        response = self.client.secrets.kv.v2.read_secret_version(
            path=self._get_transport_configuration_path(secret_reference),
        )
        if 'data' in response and 'data' in response['data'] and 'key' in response['data']['data']:
            return response['data']['data']['key']
        return None

    def delete_transport_configuration_secret(self, secret_reference: str):
        self.client.secrets.kv.delete_metadata_and_all_versions(
            self._get_transport_configuration_path(secret_reference)
        )


# Singleton for VaultClient
@lru_cache
def get_vault_client() -> VaultClient:
    return VaultClient()
