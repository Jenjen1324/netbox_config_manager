from django.shortcuts import render
from django.views import View

from netbox.views.generic import ObjectEditView, ObjectView, ObjectListView, ObjectDeleteView
from netbox_config_manager.models import ConfigTemplate
from netbox_config_manager.template_editor.forms import ConfigTemplateForm, ConfigTemplateEditorForm
from netbox_config_manager.template_editor.tables import ConfigTemplateTable


class ConfigTemplateListView(ObjectListView):
    queryset = ConfigTemplate.objects.all()
    # filterset = filtersets.VRFFilterSet
    # filterset_form = forms.VRFFilterForm
    table = ConfigTemplateTable


class ConfigTemplateView(ObjectView):
    queryset = ConfigTemplate.objects.all()
    template_name = 'netbox_config_manager/template_editor/view.html'

    class Meta:
        model = ConfigTemplate


class ConfigTemplateEditView(ObjectEditView):
    queryset = ConfigTemplate.objects.all()
    form = ConfigTemplateForm
    # template_name = 'netbox_config_manager/template_editor/edit_form.html'


class ConfigTemplateEditorView(ObjectEditView):
    queryset = ConfigTemplate.objects.all()
    form = ConfigTemplateEditorForm
    template_name = 'netbox_config_manager/template_editor/edit_form.html'


class ConfigTemplateDeleteView(ObjectDeleteView):
    queryset = ConfigTemplate.objects.all()
