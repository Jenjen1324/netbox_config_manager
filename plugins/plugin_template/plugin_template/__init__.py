from extras.plugins import PluginConfig


class PluginTemplate(PluginConfig):
    name = 'plugin_name_here'
    verbose_name = 'CHANGEME Plugin Name Here'
    description = 'CHANGEME'
    version = '0.1'
    author = 'Init7'
    author_email = 'softeng@init7.net'
    base_url = 'changeme'
    required_settings = []
    default_settings = {}


config = PluginTemplate
