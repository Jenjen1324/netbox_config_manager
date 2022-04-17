import json

from rest_framework import renderers
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import ConfigTemplateSerializer, GraphQLQuerySerializer
from ..models import ConfigTemplate, GraphQLQuery
from netbox.api.viewsets import ModelViewSet


class ConfigTemplateViewSet(ModelViewSet):
    queryset = ConfigTemplate.objects.all()
    serializer_class = ConfigTemplateSerializer


class GraphQLQueryViewSet(ModelViewSet):
    queryset = GraphQLQuery.objects.all()
    serializer_class = GraphQLQuerySerializer


class ConfigTemplateContextView(GenericAPIView):
    queryset = ConfigTemplate.objects.get_queryset()

    def get(self, request, *, template_id, object_pk):
        config_template: ConfigTemplate = self.queryset.get(id=template_id)
        data = config_template.resolve_context_data(object_pk, request)

        return Response(data)


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class CSRFExcemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        pass


class ConfigTemplatePreviewView(GenericAPIView):
    queryset = ConfigTemplate.objects.get_queryset()
    # renderer_classes = (PlainTextRenderer,)
    authentication_classes = (CSRFExcemptSessionAuthentication,)

    def post(self, request: Request):
        context_data = request.data.get('context_data', None)
        template_data = request.data.get('template_data', None)

        if context_data is None:
            return Response(data='Error: context data is empty')

        if template_data is None:
            return Response(data='Error: template data is empty')

        try:
            context_data = json.loads(context_data)
        except Exception as e:
            return Response(data='Êrror while parsing context data\n\n' + str(e))

        try:
            import jinja2
            env = jinja2.Environment()
            tmpl = env.from_string(template_data)
            return Response(data=tmpl.render(**context_data))
        except Exception as e:
            return Response(data=f'Error while rendering template:\n\n' + str(e))
