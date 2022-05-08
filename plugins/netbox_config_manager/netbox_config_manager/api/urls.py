from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from netbox.api.routers import NetBoxRouter
from . import views
from .. import simple_models

router = NetBoxRouter()

for smodel in simple_models.MODEL_REGISTRY:
    router.register(smodel.url_prefix, smodel.api_viewset)

urlpatterns = [
    path('config_template/<int:template_id>/context/<int:object_pk>', views.ConfigTemplateContextView.as_view()),
    path('config_template/preview', csrf_exempt(views.ConfigTemplatePreviewView.as_view())),
]

urlpatterns += router.urls
