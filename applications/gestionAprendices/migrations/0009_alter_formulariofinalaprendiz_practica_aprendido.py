# Generated by Django 4.2.7 on 2024-05-27 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAprendices', '0008_alter_formulariofinalaprendiz_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulariofinalaprendiz',
            name='practica_aprendido',
            field=models.CharField(max_length=2),
        ),
    ]
