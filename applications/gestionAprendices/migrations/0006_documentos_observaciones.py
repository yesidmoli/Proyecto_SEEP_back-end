# Generated by Django 4.2.7 on 2024-04-02 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAprendices', '0005_documentos_is_bitacora_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentos',
            name='observaciones',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
