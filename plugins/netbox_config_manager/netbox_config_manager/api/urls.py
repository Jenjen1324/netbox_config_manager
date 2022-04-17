from django.urls import path

from netbox.api.routers import NetBoxRouter
from netbox_config_manager.api.views import ConfigTemplateViewSet, GraphQLQueryViewSet, ConfigTemplateContextView, \
    ConfigTemplatePreviewView

from django.views.decorators.csrf import csrf_exempt

router = NetBoxRouter()
router.register('config_template', ConfigTemplateViewSet)
router.register('graphql_query', GraphQLQueryViewSet)

urlpatterns = [
    path('config_template/<int:template_id>/context/<int:object_pk>', ConfigTemplateContextView.as_view()),
    path('config_template/preview', csrf_exempt(ConfigTemplatePreviewView.as_view())),
]

urlpatterns += router.urls
