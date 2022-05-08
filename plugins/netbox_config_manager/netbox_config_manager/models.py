from typing import Dict, Optional

from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from graphql.execution import ExecutionResult

from netbox.models import NetBoxModel


class GraphQLQuery(NetBoxModel):
    name = models.CharField(max_length=50)
    query_content = models.TextField()
    context_key = models.CharField(max_length=50)

    object_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.PROTECT,
    )

    def get_absolute_url(self):
        return reverse("plugins:netbox_config_manager:graphqlquery", kwargs={"pk": self.pk})

    def execute_query(self, object_id, request=None) -> Optional[Dict]:
        from netbox.graphql.schema import schema
        result: ExecutionResult = schema.execute(self.query_content, variables={'id': object_id}, context=request)
        return result.data

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'GraphQL Query'
        verbose_name_plural = 'GraphQL Queries'


class ConfigTemplate(NetBoxModel):
    name = models.CharField(max_length=50)
    template_content = models.TextField(default='Edit Me!')
    graphql_queries = models.ManyToManyField(to=GraphQLQuery)

    def resolve_context_data(self, object_id, request=None):
        context_data = {}
        for query in self.graphql_queries.all():
            context_data[query.context_key] = query.execute_query(object_id, request)
        return context_data

    def get_absolute_url(self):
        return reverse("plugins:netbox_config_manager:configtemplate", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Configuration Template'
        verbose_name_plural = 'Configuration Templates'


class TransportConfiguration(NetBoxModel):
    class TransportType(models.TextChoices):
        SSH = 'ssh', 'ssh'
        NETCONF = 'netconf', 'netconf'

    name = models.CharField(max_length=50)
    transport_type = models.CharField(max_length=50, choices=TransportType.choices, default=TransportType.NETCONF)
    secret_reference = models.CharField(max_length=255)
    authorization_usage_users = models.ManyToManyField(to=User, related_name='transport_config_usage',
                                                       help_text='Users with usage access')
    authorization_usage_groups = models.ManyToManyField(to=Group, related_name='transport_config_usage')
    authorization_manage_users = models.ManyToManyField(to=User, related_name='transport_config_manage')
    authorization_manage_groups = models.ManyToManyField(to=Group, related_name='transport_config_manage')

    def get_absolute_url(self):
        return reverse("plugins:netbox_config_manager:transportconfiguration", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Transport Configuration'
        verbose_name_plural = 'Transport Configurations'
