from .model_helper import StandardModel
from . import models, forms, views

ConfigTemplateSModel = StandardModel(
    model=models.ConfigTemplate,
    url_name='configtemplate',
    default_fields=[
        'id', 'name', 'template_content', 'graphql_queries'
    ],
    table_linkify_field='name',
    fields_table=['id', 'name', 'graphql_queries'],
    view_display=views.ConfigTemplateView,
    form_edit=forms.ConfigTemplateForm,
)

GraphQLQuerySModel = StandardModel(
    model=models.GraphQLQuery,
    url_name='graphqlquery',
    default_fields=[
        'id', 'name', 'query_content', 'context_key', 'object_type'
    ],
    table_linkify_field='name',
    fields_table=['name', 'context_key', 'object_type'],
    form_edit=forms.GraphQLQueryForm
)

TransportConfigurationSModel = StandardModel(
    model=models.TransportConfiguration,
    url_name='transportconfiguration',
    default_fields=['id',
                    'name', 'transport_type',
                    'authorization_usage_users', 'authorization_usage_groups',
                    'authorization_manage_users', 'authorization_manage_groups'
                    ],
    table_linkify_field='name',
    form_edit=forms.TransportConfigurationForm
)

MODEL_REGISTRY = [
    ConfigTemplateSModel,
    GraphQLQuerySModel,
    TransportConfigurationSModel,
]
