from django.urls import path

from netbox.views.generic import ObjectChangeLogView, ObjectJournalView
from . import views
from ..models import ConfigTemplate

urlpatterns = [
    # ASNs
    path('', views.ConfigTemplateListView.as_view(), name='configtemplate_list'),
    path('add/', views.ConfigTemplateEditView.as_view(), name='configtemplate_add'),
    # path('import/', views.ConfigTemplateEditView.as_view(), name='config_template_import'),
    # path('edit/', views.ConfigTemplateEditView.as_view(), name='config_template_bulk_edit'),
    # path('delete/', views.ConfigTemplateEditView.as_view(), name='config_template_bulk_delete'),
    path('<int:pk>/', views.ConfigTemplateView.as_view(), name='configtemplate'),
    path('<int:pk>/edit/', views.ConfigTemplateEditView.as_view(), name='configtemplate_edit'),
    path('<int:pk>/edit_template/', views.ConfigTemplateEditorView.as_view(), name='configtemplate_edit_template'),
    path('<int:pk>/delete/', views.ConfigTemplateDeleteView.as_view(), name='configtemplate_delete'),
    path('<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='configtemplate_changelog',
         kwargs={'model': ConfigTemplate}),
    path('<int:pk>/journal/', ObjectJournalView.as_view(), name='configtemplate_journal',
         kwargs={'model': ConfigTemplate}),
]
