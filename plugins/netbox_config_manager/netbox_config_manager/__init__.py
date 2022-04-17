from extras.plugins import PluginConfig


class NetboxConfigManager(PluginConfig):
    name = 'netbox_config_manager'
    verbose_name = 'Config Manager'
    description = 'CHANGEME'
    version = '0.1'
    author = 'Init7'
    author_email = 'softeng@init7.net'
    base_url = 'config_manager'
    required_settings = []
    default_settings = {}


config = NetboxConfigManager
