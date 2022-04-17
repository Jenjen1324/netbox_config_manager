from django.contrib.contenttypes.models import ContentType

from netbox.forms import NetBoxModelForm
from netbox_config_manager.models import GraphQLQuery
from utilities.forms import ContentTypeChoiceField


class GraphQLQueryForm(NetBoxModelForm):
    object_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all()
    )


    class Meta:
        model = GraphQLQuery
        fields = ['name', 'context_key', 'object_type', 'query_content']
