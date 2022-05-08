from extras.plugins import PluginConfig


class NetboxConfigManager(PluginConfig):
    name = 'netbox_config_manager'
    verbose_name = 'Config Manager'
    description = 'CHANGEME'
    version = '0.1'
    author = 'Init7'
    author_email = 'softeng@init7.net'
    base_url = 'config_manager'
    required_settings = [
        'vault_url',
        'vault_token',
    ]
    default_settings = {
        'vault_url': None,
        'vault_token': None,
        'vault_client_cert_path': None,
        'vault_server_cert_path': None,
        'vault_namespace': None,
    }


config = NetboxConfigManager
