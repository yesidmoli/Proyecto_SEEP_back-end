# Generated by Django 4.2.7 on 2024-03-08 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAprendices', '0004_alter_aprendiz_estado_aprobacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentos',
            name='is_bitacora_check',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]