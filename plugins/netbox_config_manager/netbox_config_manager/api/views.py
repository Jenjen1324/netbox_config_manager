import json

from jinja2 import TemplateSyntaxError
from rest_framework import renderers
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import ConfigTemplate
from ..util.config_template import render_template


class ConfigTemplateContextView(GenericAPIView):
    queryset = ConfigTemplate.objects.get_queryset()

    def get(self, request, *, template_id, object_pk):
        """
        :param rest_framework.request.Request request:
        :param template_id:
        :param object_pk:
        :return:
        """
        config_template: ConfigTemplate = self.queryset.get(id=template_id)
        data = config_template.resolve_context_data(object_pk, request)

        print(request._request._get_raw_host())

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
            data = render_template(template_data, context_data)
            return Response(data=data)
        except TemplateSyntaxError as e:
            msg = f"""
            TemplateSyntaxError: {e.message}
            
            Line Number: {e.lineno}
            """
            return Response(data=msg)
        except Exception as e:
            return Response(data=f"Error: {e}")
