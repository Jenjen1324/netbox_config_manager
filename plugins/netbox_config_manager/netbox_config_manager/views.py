from netbox.views.generic import ObjectEditView, ObjectView

from . import models, forms


class ConfigTemplateView(ObjectView):
    queryset = models.ConfigTemplate.objects.all()
    template_name = 'netbox_config_manager/template_editor/view.html'

    class Meta:
        model = models.ConfigTemplate


class ConfigTemplateEditorView(ObjectEditView):
    queryset = models.ConfigTemplate.objects.all()
    form = forms.ConfigTemplateEditorForm
    template_name = 'netbox_config_manager/template_editor/edit_form.html'
