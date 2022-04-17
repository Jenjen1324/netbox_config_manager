from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_config_manager:configtemplate_list',
        link_text='Config Templates',
        buttons=()
    ),
    PluginMenuItem(
        link='plugins:netbox_config_manager:graphqlquery_list',
        link_text='GraphQL Queries',
        buttons=()
    )
)