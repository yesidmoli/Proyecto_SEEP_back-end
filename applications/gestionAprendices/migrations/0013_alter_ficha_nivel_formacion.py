# Generated by Django 4.2.7 on 2024-06-23 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAprendices', '0012_alter_aprendiz_tipo_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ficha',
            name='nivel_formacion',
            field=models.CharField(max_length=50),
        ),
    ]