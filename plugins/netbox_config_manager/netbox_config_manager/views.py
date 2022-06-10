import json

import lxml.etree
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views import View
from ncclient import manager
from netaddr import IPNetwork

from dcim.models import Device
from netbox.views.generic import ObjectEditView, ObjectView
from . import models, forms
from .util.config_template import render_template
from .vault import get_vault_client


class ConfigTemplateView(ObjectView):
    queryset = models.ConfigTemplate.objects.all()
    template_name = 'netbox_config_manager/template_editor/view.html'

    class Meta:
        model = models.ConfigTemplate


class ConfigTemplateEditorView(ObjectEditView):
    queryset = models.ConfigTemplate.objects.all()
    form = forms.ConfigTemplateEditorForm
    template_name = 'netbox_config_manager/template_editor/edit_form.html'


class ConfigTemplateGeneratorView(View):

    def get(self, request, pk: int, pk_model: int):
        config_template: models.ConfigTemplate = get_object_or_404(models.ConfigTemplate.objects.get_queryset(), pk=pk)
        context_data = config_template.resolve_context_data(pk_model, request)

        template_content = render_template(
            config_template.template_content, context_data
        )

        user: User = request.user
        from django.db.models import Q

        config_transports = models.TransportConfiguration.objects.filter(
            Q(authorization_usage_users__id__exact=user.id)
            | Q(authorization_manage_users__id__exact=user.id)
            | Q(authorization_usage_groups__user__id__exact=user.id)
            | Q(authorization_manage_groups__user__id__exact=user.id)
        )

        return render(
            request,
            'netbox_config_manager/generated_template.html',
            context={
                'object': config_template,
                'config_template': config_template,
                'content': template_content,
                'transports': config_transports,
                'pk_model': pk_model,
            }
        )


class ConfigTemplateDeployView(View):

    def get(self, request, pk: int, pk_model: int, config_transport: int):
        config_template: models.ConfigTemplate = get_object_or_404(models.ConfigTemplate.objects.get_queryset(), pk=pk)
        context_data = config_template.resolve_context_data(pk_model, request)
        device = get_object_or_404(Device.objects.get_queryset(), pk=pk_model)

        template_content = render_template(
            config_template.template_content, context_data
        )

        user: User = request.user
        from django.db.models import Q

        config_transport: models.TransportConfiguration = models.TransportConfiguration.objects.get(
            Q(authorization_usage_users__id__exact=user.id)
            | Q(authorization_manage_users__id__exact=user.id)
            | Q(authorization_usage_groups__user__id__exact=user.id)
            | Q(authorization_manage_groups__user__id__exact=user.id),
            pk=config_transport,
        )

        # Obtain Credentials
        vault = get_vault_client()
        secret_json = vault.get_transport_configuration_secret(config_transport.secret_reference)
        secret = json.loads(secret_json)

        # Write Config
        try:
            import ipam.models.ip
            ip: ipam.models.IPAddress = device.primary_ip
            addr: IPNetwork = ip.address


            netconf = manager.connect(
                host=str(addr.ip),
                port=830,
                username=secret['username'],
                password=secret['password'],
                hostkey_verify=False,
            )

            if not netconf.connected:
                raise Exception('Unable to connect to device!')

            if 'urn:ietf:params:netconf:capability:writable-running:1.0' not in netconf.server_capabilities:
                # TODO: Implement candidate datastore
                raise Exception('Device does not support writing to running configuration!')

            result = netconf.edit_config(template_content, target='running')

            netconf.close_session()

            return render(request, 'netbox_config_manager/config_written.html', {
                'object': config_template,
                'config_template': config_template,
                'result': result,
                'result_str': str(result)
            })

        except Exception as e:
            raise e


