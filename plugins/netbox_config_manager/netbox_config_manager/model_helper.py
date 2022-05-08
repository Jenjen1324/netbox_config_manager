import dataclasses
from typing import List, Optional, Type, cast

import django_tables2 as tables
from django.db import models
from django.urls import path
from django.views.generic.base import View

import netbox.models as nb_models
from netbox.api.serializers import NetBoxModelSerializer
from netbox.api.viewsets import ModelViewSet
from netbox.forms import NetBoxModelForm
from netbox.tables import NetBoxTable
from netbox.views import generic as v_generic

PLUGIN_NAME = 'netbox_config_manager'


# noinspection PyMethodMayBeStatic
@dataclasses.dataclass
class StandardModel:
    model: Type[models.Model]
    url_name: str
    default_fields: List[str]
    table_linkify_field: str
    url_prefix: str = None
    fields_table: Optional[List[str]] = None
    fields_table_visible: Optional[List[str]] = None
    fields_display: Optional[List[str]] = None
    fields_form: Optional[List[str]] = None

    table_list: Type[NetBoxTable] = None
    view_list: Optional[Type[View]] = None
    view_add: Optional[Type[View]] = None
    view_bulk_edit: Optional[Type[View]] = None
    view_bulk_delete: Optional[Type[View]] = None
    view_display: Optional[Type[View]] = None
    form_edit: Type[NetBoxModelForm] = None
    view_edit: Optional[Type[View]] = None
    view_import: Optional[Type[View]] = None
    view_delete: Optional[Type[View]] = None
    view_changelog: Optional[Type[View]] = None
    view_journal: Optional[Type[View]] = None

    api_serializer: Type[NetBoxModelSerializer] = None
    api_viewset: Type[ModelViewSet] = None
    fields_api_serializer: Optional[List[str]] = None

    def __post_init__(self):
        if self.url_prefix is None:
            self.url_prefix = self.url_name

        if self.fields_table is None:
            self.fields_table = self.default_fields
        if self.fields_table_visible is None:
            self.fields_table_visible = self.fields_table
        if self.fields_display is None:
            self.fields_display = self.default_fields
        if self.fields_form is None:
            self.fields_form = self.default_fields
        if self.fields_api_serializer is None:
            self.fields_api_serializer = list(self.default_fields)
            if 'id' not in self.fields_api_serializer:
                self.fields_api_serializer.insert(0, 'id')
            if 'display' not in self.fields_api_serializer:
                self.fields_api_serializer.insert(1, 'display')

        # Default view/table generation
        if self.table_list is None:
            self.table_list = self._table_list()
        if self.view_list is None:
            self.view_list = self._view_list()
        if self.view_add is None:
            self.view_add = self._view_add()
        # bulk_edit has no default
        # bulk_delete has no default
        if self.view_display is None:
            self.view_display = self._view_display()
        if self.form_edit is None:
            self.form_edit = self._form_edit()
        if self.view_edit is None:
            self.view_edit = self._view_edit()
        # Import has no default
        if self.view_delete is None:
            self.view_delete = self._view_delete()
        if self.view_changelog is None:
            self.view_changelog = self._view_changelog()
        if self.view_journal is None:
            self.view_journal = self._view_journal()

        if self.api_serializer is None:
            self.api_serializer = self._api_serializer()
        if self.api_viewset is None:
            self.api_viewset = self._api_viewset()

    @property
    def _class_prefix(self):
        return self.model.__name__

    def default_queryset(self):
        return self.model.objects.all()

    def _table_list(self) -> Type[NetBoxTable]:
        clazz = type(f'{self._class_prefix}Table', (NetBoxTable,), {
            self.table_linkify_field: tables.Column(linkify=True),
            'Meta': type(f'Meta', (NetBoxTable.Meta,), {
                'model': self.model,
                'fields': tuple(self.fields_table),
                'default_columns': tuple(self.fields_table_visible),
            })
        })
        return cast(Type[NetBoxTable], clazz)

    def _view_list(self) -> Type[View]:
        clazz = type(f'{self._class_prefix}ListView', (v_generic.ObjectListView,), {
            'queryset': self.default_queryset(),
            'table': self._table_list()
        })
        return cast(Type[v_generic.ObjectListView], clazz)

    def _view_add(self) -> Optional[Type[View]]:
        return self._view_edit()

    def _view_display(self) -> Type[View]:
        def context_function(_, __, instance: models.Model):
            field_data = []
            for field_name in self.fields_display:
                field = self.model._meta.get_field(field_name)
                field_data.append({
                    'name': field.name,
                    'value': getattr(instance, field_name)
                })
            return {
                'fields': field_data
            }

        clazz = type(f'{self._class_prefix}', (v_generic.ObjectView,), {
            'queryset': self.default_queryset(),
            'template_name': f'{PLUGIN_NAME}/default_view.html',
            'get_extra_context': context_function
        })
        return cast(Type[v_generic.ObjectView], clazz)

    def _form_edit(self) -> Type[NetBoxModelForm]:
        clazz = type(f'{self._class_prefix}Form', (NetBoxModelForm,), {
            'Meta': type('Meta', (), {
                'model': self.model,
                'fields': tuple(self.fields_form),
            })
        })
        return cast(Type[NetBoxModelForm], clazz)

    def _view_edit(self) -> Type[View]:
        clazz = type(f'{self._class_prefix}EditView', (v_generic.ObjectEditView,), {
            'queryset': self.default_queryset(),
            'form': self.form_edit
        })
        return cast(Type[v_generic.ObjectEditView], clazz)

    def _view_delete(self) -> Type[View]:
        clazz = type(f'{self._class_prefix}DeleteView', (v_generic.ObjectDeleteView,), {
            'queryset': self.default_queryset(),
        })
        return cast(Type[v_generic.ObjectDeleteView], clazz)

    def _view_changelog(self) -> Optional[Type[View]]:
        if not issubclass(self.model, nb_models.ChangeLoggingMixin):
            return None
        clazz = type(f'{self._class_prefix}ChangeLogView', (v_generic.ObjectChangeLogView,), {
            'base_template': f'{PLUGIN_NAME}/default_view.html'
        })
        return cast(Type[v_generic.ObjectChangeLogView], clazz)

    def _view_journal(self) -> Optional[Type[View]]:
        if not issubclass(self.model, nb_models.JournalingMixin):
            return None
        clazz = type(f'{self._class_prefix}JournalView', (v_generic.ObjectJournalView,), {
            'base_template': f'{PLUGIN_NAME}/default_view.html'
        })
        return cast(Type[v_generic.ObjectJournalView], clazz)

    def _api_serializer(self) -> Type[NetBoxModelSerializer]:
        clazz = type(f'{self._class_prefix}Serializer', (NetBoxModelSerializer,), {
            'Meta': type('Meta', (), {
                'model': self.model,
                'fields': self.fields_api_serializer,
            })
        })
        return cast(Type[NetBoxModelSerializer], clazz)

    def _api_viewset(self) -> Type[ModelViewSet]:
        clazz = type(f'{self._class_prefix}ViewSet', (ModelViewSet,), {
            'queryset': self.default_queryset(),
            'serializer_class': self.api_serializer,
        })
        return cast(Type[ModelViewSet], clazz)

    def generate_urls(self) -> List:
        patterns = []

        def add_opt_pattern(url: str, view: Type[View], suffix: str, kwargs=None):
            nonlocal patterns
            if view:
                patterns.append(path(url, view.as_view(), name=f'{self.url_name}{suffix}', kwargs=kwargs))

        add_opt_pattern('', self.view_list, '_list')
        add_opt_pattern('add/', self.view_add, '_add')
        add_opt_pattern('import/', self.view_import, '_import')
        add_opt_pattern('edit/', self.view_bulk_edit, '_bulk_edit')
        add_opt_pattern('delete/', self.view_bulk_delete, '_bulk_delete')

        add_opt_pattern('<int:pk>/', self.view_display, '')
        add_opt_pattern('<int:pk>/edit/', self.view_edit, '_edit')
        add_opt_pattern('<int:pk>/delete/', self.view_delete, '_delete')
        add_opt_pattern('<int:pk>/changelog/', self.view_changelog, '_changelog',
                        kwargs={'model': self.model})
        add_opt_pattern('<int:pk>/journal/', self.view_journal, '_journal',
                        kwargs={'model': self.model})
        return patterns

    def generate_navigation(self):
        from extras.plugins import PluginMenuButton
        from extras.plugins import PluginMenuItem
        from utilities.choices import ButtonColorChoices
        buttons = list()
        buttons.append(PluginMenuButton(
            f'plugins:{PLUGIN_NAME}:{self.url_name}_add',
            'Add',
            'mdi mdi-plus-thick',
            ButtonColorChoices.GREEN))

        if self.view_import:
            buttons.append(PluginMenuButton(
                f'plugins:{PLUGIN_NAME}:{self.url_name}_import',
                'Import',
                'mdi mdi-upload',
                ButtonColorChoices.BLUE))
        return PluginMenuItem(
            f'plugins:{PLUGIN_NAME}:{self.url_name}_list',
            self.model._meta.verbose_name_plural,
            buttons=tuple(buttons)
        )
