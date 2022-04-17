from netbox.tables import NetBoxTable
from netbox_config_manager.models import GraphQLQuery
import django_tables2 as tables


class GraphQLQueryTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = GraphQLQuery
        fields = ('pk', 'name')
        default_columns = ('pk', 'name')
