# Generated by Django 4.2.7 on 2024-02-29 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestionAprendices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_actividad', models.CharField(max_length=100)),
                ('tiene_evidencia_aprendizaje', models.BooleanField()),
                ('fecha_recoleccion_evidencia', models.DateField(blank=True, null=True)),
                ('lugar_recoleccion_evidencia', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('juicio_evaluacion', models.CharField(max_length=100)),
                ('reconocimientos_especiales', models.BooleanField()),
                ('reconocimientos_detalle', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_enteconformador', models.CharField(max_length=100)),
                ('firma_enteconformador', models.TextField(max_length=255)),
                ('firma_aprendiz', models.TextField(max_length=255)),
                ('nombre_instructor', models.CharField(max_length=100)),
                ('firma_instructor', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FactorActitudinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('satisfactorio', models.BooleanField(default=False)),
                ('observacion', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FactorTecnico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('satisfactorio', models.BooleanField(default=False)),
                ('observacion', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Seguimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_informe', models.CharField(max_length=50)),
                ('periodo_evaluado_inicio', models.DateField()),
                ('periodo_evaluado_final', models.DateField()),
                ('observaciones_ente_conformador', models.TextField()),
                ('observaciones_aprendiz', models.TextField(max_length=250)),
                ('factores_actitudinales', models.ManyToManyField(related_name='seguimientos', to='formatos.factoractitudinal')),
                ('factores_tecnicos', models.ManyToManyField(related_name='seguimientos', to='formatos.factortecnico')),
            ],
        ),
        migrations.CreateModel(
            name='Planeacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('nombre_enteconformador', models.CharField(max_length=100)),
                ('firma_enteconformador', models.TextField()),
                ('firma_aprendiz', models.TextField()),
                ('nombre_instructor', models.CharField(max_length=100)),
                ('firma_instructor', models.TextField(max_length=255)),
                ('actividades', models.ManyToManyField(related_name='actividades', to='formatos.actividades')),
            ],
        ),
        migrations.CreateModel(
            name='FormatoPlaneacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=100)),
                ('fecha_elaboracion', models.DateField()),
                ('aprendiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formatos_planeacion', to='gestionAprendices.aprendiz')),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formato_planeacion', to='formatos.evaluacion')),
                ('planeacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formato_planeacion', to='formatos.planeacion')),
                ('seguimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formato_planeacion', to='formatos.seguimiento')),
            ],
        ),
    ]