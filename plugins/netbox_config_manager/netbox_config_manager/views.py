from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views import View

from netbox.views.generic import ObjectEditView, ObjectView
from . import models, forms
from .util.config_template import render_template


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
                'transports': config_transports
            }
        )
