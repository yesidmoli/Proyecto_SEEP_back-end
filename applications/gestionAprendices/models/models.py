from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from users.models import User

class InstructorEncargado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=20)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)

    ficha = models.ManyToManyField('Ficha' ,related_name="instructores")


    class Meta:
        verbose_name = "Instructor encargado"
        verbose_name_plural = "Instructores Encargados"

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
    

# Creamos el modelo que contendra los datos de la ficha
class Ficha(models.Model):
   
    NIVEL_FORMACION_CHOICES = (
        ('Tecnico', 'Técnico'),
        ('Tecnologo', 'Tecnólogo'),
        
  
    )

    HORARIO_FORMACION_CHOICES = (
        ('Mixta', 'Mixta'),
        ('Diurna', 'Diurna'),
        
    )

    numero_ficha = models.CharField(max_length=20 )
    nombre_programa = models.CharField(max_length=100)
    nivel_formacion = models.CharField(max_length=50)
    horario_formacion = models.CharField(max_length=50, choices=HORARIO_FORMACION_CHOICES)
   

    

    class Meta:
        verbose_name = "Ficha"
        verbose_name_plural = "Fichas"
    

    def __str__(self):
        return  f'{self.numero_ficha } - {self.id}'


class Aprendiz(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    ESTADO_APROBACION_CHOICES = (
        ('aprobado', 'Aprobado'),
        ('no_aprobado', 'No aprobado'),
        ('pendiente', 'Pendiente'),
    )

    TIPO_DOCUMENTO = (
        ('CC', 'CC'),
        ('TI', 'TI')
    )
    # Información personal
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=20 )
    numero_documento = models.CharField(max_length=20, unique=True)
    fecha_expedicion = models.DateField()
    lugar_expedicion = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=10)
    
    # Información de contacto
    direccion_domicilio = models.TextField()
    municipio = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    numero_celular1 = models.CharField(max_length=20)
    numero_celular2 = models.CharField(max_length=20, null=True, blank=True)
    telefono_fijo = models.CharField(max_length=20, null=True, blank=True)
    correo_principal = models.EmailField()
    correo_secundario = models.EmailField(null=True, blank=True)
    
    # Otras características
    finalizacion_etapa_lectiva = models.DateField()
    estado_aprobacion = models.CharField(max_length=50, default="pendiente", blank=True)
    
    # Relación con la tabla Empresa (ForeignKey)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)

    # Relación con la tabla Ficha (ForeignKey)
    ficha = models.ForeignKey('Ficha', on_delete=models.CASCADE, related_name='aprendiz')


    class Meta:
        verbose_name = "Aprendiz"
        verbose_name_plural = "Aprendices"
    

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
    

class Empresa(models.Model):
    nit = models.CharField(max_length=20, blank=True)
    razon_social = models.CharField(max_length=100, blank=True)
    nombre_jefe_inmediato = models.CharField(max_length=100, blank=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank= True)
    cargo = models.CharField(max_length=100, blank= True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return f'{self.razon_social}'
    
class DocumentacionAprendiz(models.Model):
    # Relación con el aprendiz
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE, related_name='documentacion_aprendiz')

    # Campos de documentos
    documento_identidad = models.FileField(upload_to='documentos/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)
    carta_laboral = models.FileField(upload_to='documentos/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)
    certificado_agencia_publica = models.FileField(upload_to='documentos/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)
    pruebas_tyt = models.FileField(upload_to='documentos/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)
    carnet_destruido = models.FileField(upload_to='documentos/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)
    formato_bitacoras = models.FileField(upload_to='documentos/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)

    # Relación con el instructor encargado
    instructor_encargado = models.ForeignKey(InstructorEncargado, on_delete=models.CASCADE, related_name='documentacion_instructor')

    def __str__(self):
        return f'Documentación de {self.aprendiz}'


#modelo para guardar cada documento como una instancia
class Documentos(models.Model):
    
    tipo_documento = models.CharField(max_length=30)
    archivo = models.FileField(upload_to='documentos/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    is_bitacora = models.BooleanField(default = False, blank = True, null = True)
    is_bitacora_check = models.BooleanField(default = False, blank = True, null = True)
    observaciones = models.CharField(max_length=255 , blank = True, null = True)
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE, related_name='documentos')



    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
    def __str__(self):
        return f'{self.tipo_documento} - {self.aprendiz}'


class FormularioFinalAprendiz(models.Model):
    OPCIONES_CHOICES = (
        ('SI', 'Si'),
        ('NO', 'No'),
    )
    
    CARGO_CHOICES = (
        ('EMPLEADO', 'Empleado'),
        ('INDEPENDIENTE', 'Independiente'),
    )
    
    TIPO_ESTUDIO_CHOICES = (
        ('TÉCNICO', 'Técnico'),
        ('TECNOLÓGICO', 'Tecnológico'),
        ('UNIVERSITARIO', 'Universitario'),
        ('OTRO', 'Otro'),
    )

    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE, related_name='formulario_final')
    madre_cabeza_familia = models.BooleanField(default=False , blank = True, null = True)
    titulo_obtenido = models.CharField(max_length=100 , blank = True, null = True)
    fecha_fin_etapa_lectiva = models.DateField()
    cargo_funciones = models.CharField(max_length=100)
    fecha_fin_etapa_productiva = models.DateField()
    practica_aprendido = models.CharField(max_length=50)
    estudios_superiores_adicionales = models.CharField(max_length=2, choices=OPCIONES_CHOICES)
    estudios = models.CharField(max_length=100, blank=True, null=True)
    trabaja_actualmente = models.CharField(max_length=2, choices=OPCIONES_CHOICES)
    estado_actual = models.CharField(max_length=20)
    cargo_actual = models.CharField(max_length=100, blank=True, null=True)
    empresa_labora = models.CharField(max_length=100, blank=True, null=True)
    antiguedad_trabajo = models.PositiveIntegerField(blank=True, null=True)
    area_informacion_complementaria = models.CharField(max_length=100)
    actualmente_estudia = models.CharField(max_length=2, choices=OPCIONES_CHOICES)
    estudia_que = models.CharField(max_length=100, blank=True, null=True)
    institucion_universidad = models.CharField(max_length=100, blank=True, null=True)
    certificar_competencias_laborales = models.CharField(max_length=2, choices=OPCIONES_CHOICES)
    conoce_beneficios_sena = models.CharField(max_length=2, choices=OPCIONES_CHOICES)
    idea_negocio = models.CharField(max_length=2, choices=OPCIONES_CHOICES)
    conoce_servicio_fondo_emprender = models.CharField(max_length=2, choices=OPCIONES_CHOICES)
    necesita_empleo = models.CharField(max_length=2, choices=OPCIONES_CHOICES)
    sugerencias_comentarios = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Formulario final del aprendiz"
        verbose_name_plural = "Formularios finales de los aprendices"
   