from django.forms import ModelForm, Widget, Textarea, CharField

from netbox.forms import NetBoxModelForm
from netbox_config_manager.models import ConfigTemplate, GraphQLQuery
from utilities.forms import DynamicModelMultipleChoiceField


class AceEditorField(Widget):
    template_name = 'netbox_config_manager/components/field_code_editor.html'


class ConfigTemplateEditorForm(NetBoxModelForm):
    template_content = CharField(widget=AceEditorField)

    class Meta:
        model = ConfigTemplate
        fields = ('template_content',)


class ConfigTemplateForm(NetBoxModelForm):
    graphql_queries = DynamicModelMultipleChoiceField(
        queryset=GraphQLQuery.objects.all(),
        required=False,
        # to_field_name='name'
    )

    class Meta:
        model = ConfigTemplate
        fields = ['name', 'graphql_queries']
