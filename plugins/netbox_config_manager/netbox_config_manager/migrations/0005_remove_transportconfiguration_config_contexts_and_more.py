# Generated by Django 4.0.3 on 2022-05-08 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_config_manager', '0004_alter_graphqlquery_options_transportconfiguration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transportconfiguration',
            name='config_contexts',
        ),
        migrations.AddField(
            model_name='transportconfiguration',
            name='transport_type',
            field=models.CharField(default='netconf', max_length=50),
        ),
    ]