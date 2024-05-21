
from django.db import models
from applications.gestionAprendices.models.models import Aprendiz, InstructorEncargado

#modelo para el agendamiento de visitas
class Visita(models.Model):
    """
    Represents a visit made by an apprentice to an instructor.

    Attributes:
        TIPOS_DE_VISITA (tuple): Choices for the type of visit.
        ESTADOS_DE_VISITA (tuple): Choices for the state of the visit.
        NUMERO_DE_VISITA_CHOICES (tuple): Choices for the visit number.
        fecha_visita (DateField): The date of the visit.
        hora_visita (TimeField): The time of the visit.
        tipo_visita (CharField): The type of visit.
        lugar (CharField): The location of the visit.
        numero_visita (IntegerField): The number of the visit.
        estado (CharField): The state of the visit.
        aprendiz (ForeignKey): The apprentice associated with the visit.
        instructor_encargado (ForeignKey): The instructor in charge of the visit.
        observaciones (TextField): Additional observations for the visit.
        motivo_cancelacion (TextField): The reason for canceling the visit.
        fecha_cancelacion (DateTimeField): The date and time of the cancellation.
    """

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
    aprendiz = models.ForeignKey(Aprendiz, related_name="visita",on_delete=models.CASCADE)
    instructor_encargado = models.ForeignKey(InstructorEncargado, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    motivo_cancelacion = models.TextField(blank=True, null=True)
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
   

    
    def __str__(self):
        return f' id  {self.id} Visita de {self.aprendiz} ({self.fecha_visita})'
    
    class Meta:
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"
