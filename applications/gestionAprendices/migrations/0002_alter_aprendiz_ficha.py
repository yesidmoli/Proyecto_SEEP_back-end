# Generated by Django 4.2.7 on 2023-11-04 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAprendices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aprendiz',
            name='ficha',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aprendiz', to='gestionAprendices.ficha'),
        ),
    ]
