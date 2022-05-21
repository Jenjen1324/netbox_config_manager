from django.contrib.contenttypes.models import ContentType

from extras.plugins import PluginTemplateExtension
from . import models


class TemplateGenerationButtons(PluginTemplateExtension):
    model = 'dcim.device'

    def buttons(self):
        try:
            content_type = ContentType.objects.get(app_label='dcim', model='device')
            templates = models.ConfigTemplate.objects.filter(
                graphql_queries__object_type=content_type
            )
            return self.render('netbox_config_manager/extensions/template_generation_button.html', {'templates': templates})
        except Exception as e:
            print(e)
        return ''


template_extensions = [TemplateGenerationButtons]
