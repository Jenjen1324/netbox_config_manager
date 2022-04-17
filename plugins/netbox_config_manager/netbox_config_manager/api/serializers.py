from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from netbox_config_manager.models import ConfigTemplate, GraphQLQuery

from netbox.api.serializers import NetBoxModelSerializer


class ConfigTemplateSerializer(NetBoxModelSerializer):

    class Meta:
        model = ConfigTemplate
        fields = ['id', 'name', 'display', 'template_content']



class GraphQLQuerySerializer(NetBoxModelSerializer):

    class Meta:
        model = GraphQLQuery
        fields = ['id', 'name', 'display','query_content', 'object_type']
