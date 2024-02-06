
from django.db import models
from applications.gestionAprendices.models import Aprendiz, InstructorEncargado

class Visita(models.Model):
    TIPOS_DE_VISITA = (
        ('presencial', 'Visita Presencial'),
        ('virtual', 'Visita Virtual'),
    )
    
    ESTADOS_DE_VISITA = (
        ('programada', 'Programada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
        
    )

    NUMERO_DE_VISITA_CHOICES = (
        (1, 'Visita 1'),
        (2, 'Visita 2'),
        (3, 'Visita 3'),
    )

    fecha_visita = models.DateField()
    hora_visita = models.TimeField()
    tipo_visita = models.CharField(max_length=10, choices=TIPOS_DE_VISITA)
    lugar = models.CharField(max_length=255)
    numero_visita = models.IntegerField(choices=NUMERO_DE_VISITA_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADOS_DE_VISITA)
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
    instructor_encargado = models.ForeignKey(InstructorEncargado, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')



    # Campos adicionales para el registro de visitas canceladas
    motivo_cancelacion = models.TextField(blank=True, null=True)
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
   

    
    def __str__(self):
        return f' id  {self.id} Visita de {self.aprendiz} ({self.fecha_visita})'
    
    class Meta:
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"
