# Generated by Django 4.2.7 on 2024-02-29 17:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aprendiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('tipo_documento', models.CharField(choices=[('CC', 'CC'), ('TI', 'TI')], max_length=20)),
                ('numero_documento', models.CharField(max_length=20, unique=True)),
                ('fecha_expedicion', models.DateField()),
                ('lugar_expedicion', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('sexo', models.CharField(max_length=10)),
                ('direccion_domicilio', models.TextField()),
                ('municipio', models.CharField(max_length=100)),
                ('departamento', models.CharField(max_length=100)),
                ('numero_celular1', models.CharField(max_length=20)),
                ('numero_celular2', models.CharField(blank=True, max_length=20, null=True)),
                ('telefono_fijo', models.CharField(blank=True, max_length=20, null=True)),
                ('correo_principal', models.EmailField(max_length=254)),
                ('correo_secundario', models.EmailField(blank=True, max_length=254, null=True)),
                ('finalizacion_etapa_lectiva', models.DateField()),
                ('estado_aprobacion', models.CharField(choices=[('aprobado', 'Aprobado'), ('no_aprobado', 'No aprobado'), ('pendiente', 'Pendiente')], max_length=50)),
            ],
            options={
                'verbose_name': 'Aprendiz',
                'verbose_name_plural': 'Aprendices',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit', models.CharField(blank=True, max_length=20)),
                ('razon_social', models.CharField(blank=True, max_length=100)),
                ('nombre_jefe_inmediato', models.CharField(blank=True, max_length=100)),
                ('correo', models.EmailField(blank=True, max_length=254)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('direccion', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Ficha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_ficha', models.CharField(max_length=20)),
                ('nombre_programa', models.CharField(max_length=100)),
                ('nivel_formacion', models.CharField(choices=[('Tecnico', 'Técnico'), ('Tecnologo', 'Tecnólogo')], max_length=50)),
                ('horario_formacion', models.CharField(choices=[('Mixta', 'Mixta'), ('Diurna', 'Diurna')], max_length=50)),
            ],
            options={
                'verbose_name': 'Ficha',
                'verbose_name_plural': 'Fichas',
            },
        ),
        migrations.CreateModel(
            name='InstructorEncargado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('numero_documento', models.CharField(max_length=20)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=20)),
                ('ficha', models.ManyToManyField(related_name='instructores', to='gestionAprendices.ficha')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Instructor encargado',
                'verbose_name_plural': 'Instructores Encargados',
            },
        ),
        migrations.CreateModel(
            name='Documentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_documento', models.CharField(max_length=30)),
                ('archivo', models.FileField(upload_to='documentos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('is_bitacora', models.BooleanField(blank=True, default=False, null=True)),
                ('aprendiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='gestionAprendices.aprendiz')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
            },
        ),
        migrations.CreateModel(
            name='DocumentacionAprendiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento_identidad', models.FileField(blank=True, null=True, upload_to='documentos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('carta_laboral', models.FileField(blank=True, null=True, upload_to='documentos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('certificado_agencia_publica', models.FileField(blank=True, null=True, upload_to='documentos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('pruebas_tyt', models.FileField(blank=True, null=True, upload_to='documentos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('carnet_destruido', models.FileField(blank=True, null=True, upload_to='documentos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('formato_bitacoras', models.FileField(blank=True, null=True, upload_to='documentos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('aprendiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentacion_aprendiz', to='gestionAprendices.aprendiz')),
                ('instructor_encargado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentacion_instructor', to='gestionAprendices.instructorencargado')),
            ],
        ),
        migrations.AddField(
            model_name='aprendiz',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionAprendices.empresa'),
        ),
        migrations.AddField(
            model_name='aprendiz',
            name='ficha',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aprendiz', to='gestionAprendices.ficha'),
        ),
        migrations.AddField(
            model_name='aprendiz',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
