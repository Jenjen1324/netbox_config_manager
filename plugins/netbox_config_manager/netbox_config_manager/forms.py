import json
import uuid

from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

import utilities
from netbox.forms import NetBoxModelForm
from utilities.forms import ContentTypeChoiceField
from utilities.forms import widgets
from . import models, vault


class GraphQLQueryForm(NetBoxModelForm):
    object_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all()
    )

    class Meta:
        model = models.GraphQLQuery
        fields = ['name', 'context_key', 'object_type', 'query_content']


class AceEditorField(forms.Widget):
    template_name = 'netbox_config_manager/components/field_code_editor.html'


class ConfigTemplateEditorForm(NetBoxModelForm):
    template_content = forms.CharField(widget=AceEditorField)

    class Meta:
        model = models.ConfigTemplate
        fields = ('template_content',)


class ConfigTemplateForm(NetBoxModelForm):
    graphql_queries = utilities.forms.DynamicModelMultipleChoiceField(
        queryset=models.GraphQLQuery.objects.all(),
        required=False,
    )

    class Meta:
        model = models.ConfigTemplate
        fields = ['name', 'graphql_queries']


class TransportConfigurationForm(NetBoxModelForm):
    username = forms.CharField(label='Username', required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)

    authorization_usage_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=widgets.StaticSelectMultiple,
        label='Users with usage access',
        required=False,

    )
    authorization_usage_groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=widgets.StaticSelectMultiple,
        label='Groups with usage access',
        required=False,
    )
    authorization_manage_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=widgets.StaticSelectMultiple,
        label='Users with write access',
        required=False,
    )
    authorization_manage_groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=widgets.StaticSelectMultiple,
        label='Groups with write access',
        required=False,
    )

    def clean(self):
        super().clean()

        instance: models.TransportConfiguration = self.instance
        if not instance.secret_reference:
            instance.secret_reference = str(uuid.uuid4())

        vault_client = vault.get_vault_client()

        if not self.cleaned_data['password']:
            # No password is set, check if the secret already has data
            previous_secret = vault_client.get_transport_configuration_secret(instance.secret_reference)
            if not previous_secret:
                self.add_error('password', 'Password required for new fields')
                return
            else:
                self.cleaned_data['secret_data'] = json.loads(previous_secret)
        else:
            self.cleaned_data['secret_data'] = json.dumps({
                'username': self.cleaned_data['username'],
                'password': self.cleaned_data['password'],
            })

    def save(self, commit=True):
        instance = super().save(commit=False)

        vault_client = vault.get_vault_client()
        vault_client.put_transport_configuration_secret(
            instance.secret_reference,
            self.cleaned_data['secret_data']
        )

        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.TransportConfiguration
        fields = ('name', 'transport_type',
                  'authorization_usage_users', 'authorization_usage_groups',
                  'authorization_manage_users', 'authorization_manage_groups')
