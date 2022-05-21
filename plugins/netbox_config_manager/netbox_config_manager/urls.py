from django.urls import path, include

from . import views, simple_models

urlpatterns = [
    path('configtemplate/<int:pk>/edit_template/', views.ConfigTemplateEditorView.as_view(),
         name='configtemplate_edit_template'),
    path('configtemplate/<int:pk>/generate/<int:pk_model>', views.ConfigTemplateGeneratorView.as_view(),
         name='configtemplate_render_template')
]

for simple_model in simple_models.MODEL_REGISTRY:
    urlpatterns.append(path(f'{simple_model.url_prefix}/', include(simple_model.generate_urls())))
