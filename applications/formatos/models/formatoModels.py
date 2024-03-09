from django.db import models
from applications.gestionAprendices.models.models import Aprendiz



#creamos un modelo abstracto para los diferentes factores de  la parte de seguimiento del formato
class Factor(models.Model):
    variable = models.CharField(max_length=100)
    descripcion = models.TextField()
    satisfactorio = models.BooleanField(default=False)
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

class FactorActitudinal(Factor):
    pass

class FactorTecnico(Factor):
    pass


class Seguimiento(models.Model):
    tipo_informe = models.CharField(max_length=50, blank= True, null = True)
    periodo_evaluado_inicio = models.DateField(blank= True, null = True)
    periodo_evaluado_final = models.DateField(blank= True, null = True)
    observaciones_ente_conformador = models.TextField(max_length= 250, blank= True, null = True)
    observaciones_aprendiz = models.TextField(max_length=250, blank= True, null = True)
    factores_actitudinales = models.ManyToManyField('FactorActitudinal', related_name='seguimientos')
    factores_tecnicos = models.ManyToManyField('FactorTecnico', related_name='seguimientos')


class Evaluacion(models.Model):
    juicio_evaluacion = models.CharField(max_length=100, blank= True, null = True)
    reconocimientos_especiales = models.BooleanField(blank= True, null = True)
    reconocimientos_detalle = models.TextField( null=True, blank=True)
    nombre_enteconformador = models.CharField(max_length=100, blank= True, null = True)
    firma_enteconformador = models.TextField(blank= True, null = True)
    firma_aprendiz = models.TextField(blank= True, null = True)
    nombre_instructor = models.CharField(max_length=100, blank= True, null = True)
    firma_instructor = models.TextField(blank= True, null = True)

class Planeacion(models.Model):
    observaciones = models.TextField(null=True, blank=True)
    nombre_enteconformador = models.CharField(max_length=100, blank= True, null = True)
    firma_enteconformador = models.TextField(blank= True, null = True)
    firma_aprendiz = models.TextField(blank= True, null = True)
    nombre_instructor = models.CharField(max_length=100, blank= True, null = True)
    firma_instructor = models.TextField(blank= True, null = True)
    actividades = models.ManyToManyField('Actividades', related_name='actividades')

class Actividades(models.Model):
    nombre_actividad = models.CharField(max_length=100, blank= True, null = True)
    tiene_evidencia_aprendizaje = models.BooleanField(blank= True, null = True)
    fecha_recoleccion_evidencia = models.DateField(null=True, blank=True)
    lugar_recoleccion_evidencia = models.CharField(max_length=100, blank= True, null = True)
   


class FormatoPlaneacion(models.Model):
    ciudad = models.CharField(max_length=100 , blank= True)
    fecha_elaboracion = models.DateField(blank= True, null = True)
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE, related_name='formatos_planeacion')
    planeacion = models.ForeignKey(Planeacion, on_delete=models.CASCADE, related_name='formato_planeacion')
    seguimiento = models.ForeignKey(Seguimiento, on_delete=models.CASCADE, related_name='formato_planeacion')
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='formato_planeacion')

# from django.db import models
# from applications.gestionAprendices.models.models import Aprendiz


# # Creamos un modelo abstracto para los diferentes factores de la parte de seguimiento del formato
# class Factor(models.Model):
#     variable = models.CharField(max_length=100)
#     descripcion = models.TextField()
#     satisfactorio = models.BooleanField(default=False)
#     observacion = models.TextField(blank=True, null=True)

#     class Meta:
#         abstract = True

# class FactorActitudinal(Factor):
#     pass

# class FactorTecnico(Factor):
#     pass


# class Seguimiento(models.Model):
#     tipo_informe = models.CharField(max_length=50)
#     periodo_evaluado_inicio = models.DateField()
#     periodo_evaluado_final = models.DateField()
#     observaciones_ente_conformador = models.TextField()
#     observaciones_aprendiz = models.TextField()
#     formato_planeacion = models.ForeignKey('FormatoPlaneacion', on_delete=models.CASCADE, related_name='seguimientos')

# class Evaluacion(models.Model):
#     juicio_evaluacion = models.CharField(max_length=100)
#     reconocimientos_especiales = models.BooleanField()
#     reconocimientos_detalle = models.CharField(max_length=255, null=True, blank=True)
#     nombre_firma_enteconformador = models.CharField(max_length=100)
#     firma_enteconformador = models.TextField()
#     firma_aprendiz = models.TextField()
#     nombre_firma_instructor = models.CharField(max_length=100)
#     firma_instructor = models.TextField()
#     formato_planeacion = models.ForeignKey('FormatoPlaneacion', on_delete=models.CASCADE, related_name='evaluaciones')

# class Planeacion(models.Model):
#     observaciones = models.TextField()
#     nombre_enteconformador = models.CharField(max_length=100)
#     firma_enteconformador = models.TextField()
#     firma_aprendiz = models.TextField()
#     nombre_firma_instructor = models.CharField(max_length=100)
#     firma_instructor = models.TextField()
#     formato_planeacion = models.ForeignKey('FormatoPlaneacion', on_delete=models.CASCADE, related_name='planeaciones')

# class Actividades(models.Model):
#     nombre_actividad = models.CharField(max_length=100)
#     tiene_evidencia_aprendizaje = models.BooleanField()
#     fecha_recoleccion_evidencia = models.DateField(null=True, blank=True)
#     lugar_recoleccion_evidencia = models.CharField(max_length=100)
#     planeacion = models.ForeignKey('Planeacion', on_delete=models.CASCADE, related_name='actividades')

# class FormatoPlaneacion(models.Model):
#     ciudad = models.CharField(max_length=100)
#     fecha_elaboracion = models.DateField()
#     aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE, related_name='formatos_planeacion')
