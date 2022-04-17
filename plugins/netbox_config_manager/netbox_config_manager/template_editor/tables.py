from netbox_config_manager.models import ConfigTemplate

from netbox.tables import NetBoxTable
import django_tables2 as tables


class ConfigTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ConfigTemplate
        fields = ('pk', 'name')
        default_columns = ('pk', 'name')