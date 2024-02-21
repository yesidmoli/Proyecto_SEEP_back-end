"""Importamos el serializers, para poder trabajar con los json"""
from rest_framework import serializers, pagination

from rest_framework.exceptions import ValidationError

from applications.agendarcitas.models.visita import Visita
from applications.gestionAprendices.serializers.AprendizSerializer import PerfilAprendiz

from datetime import date

# from ...gestionAprendices.serializers.serializers import AprendizBasicSerializer

class VisitSerializer(serializers.ModelSerializer):
    # aprendiz = AprendizBasicSerializer ()
    aprendiz_datos = PerfilAprendiz(source='aprendiz', read_only=True)
    
    motivo_cancelacion = serializers.CharField(
        allow_blank=True, required=False, write_only=True,
        help_text='Motivo de la cancelación de la visita.'
    )
    fecha_cancelacion = serializers.DateTimeField(
        read_only=True
    )
    
    class Meta:

        model = Visita
        fields = ('__all__')
        

class NumeroVisitaAprendizSerializer(serializers.ModelSerializer):
    # motivo_cancelacion = serializers.CharField(
    #     allow_blank=True, required=False, write_only=True,
    #     help_text='Motivo de la cancelación de la visita.'
    # )
    # fecha_cancelacion = serializers.DateTimeField(
    #     read_only=True
    # )


    class Meta:
        model = Visita
        fields = '__all__'   

 

#validaciones
    def validate(self, data):

        #validacion para que no se programe una visita a la misma hora
        fecha_visita = data.get('fecha_visita')
        hora_visita = data.get('hora_visita')

        # Obtemos la fecha actual
        fecha_actual = date.today()

        # Verifica si la fecha de la visita es una fecha futura
        if fecha_visita < fecha_actual:
            raise ValidationError('No se pueden programar visitas en fechas pasadas.')



        #verifica si el estado de una nueva visita es "Programada" y luego buscamos si existen visitas realizadas para el mismo aprendiz. 
        # Si no se encuentran visitas realizadas, se genera un error de validación, lo que impide la programación de la segunda visita. y asi mismo con la tercera
        aprendiz = data.get('aprendiz')
        estado = data.get('estado')
        numero_visita = data.get('numero_visita')

        # Obtén todas las visitas programadas y realizadas del aprendiz para la visita en cuestión
        visitas_programadas = Visita.objects.filter(aprendiz=aprendiz, estado='programada', numero_visita=numero_visita)
        visitas_realizadas = Visita.objects.filter(aprendiz=aprendiz, estado='realizada', numero_visita=numero_visita)

        if estado == 'programada':
            # Verifica si ya se programó una visita
            if visitas_programadas.exists():
                raise ValidationError(f'El aprendiz ya  tiene una visita programada de número {numero_visita}.')
            
            # Verifica que no se exceda el límite de 3 visitas de un mismo número
            if visitas_programadas.count() >= 1:
                raise ValidationError(f'No puedes programar más de una visita de número {numero_visita}.')
            

            
        elif estado == 'realizada':
            # Verifica que haya una visita programada para marcar como "Realizada"
            if visitas_programadas.count() == 0:
                raise ValidationError(f'No puedes marcar una visita de número {numero_visita} como "Realizada" si no hay visitas programadas previamente.')

            # Verifica que no se exceda el límite de 3 visitas en total
            if visitas_programadas.count() + visitas_realizadas.count() >= 3:
                raise ValidationError('No puedes programar más de tres visitas en total.')
                            

        # Verifica si ya existe una visita con la misma fecha pero hora diferente
        visitas_existente = Visita.objects.filter(fecha_visita=fecha_visita)

        for visita in visitas_existente:
            if visita.hora_visita == hora_visita:
                raise ValidationError('La hora ya está programada para otra visita en la misma fecha.')

        return data


class AprendizVisitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Visita
        fields = ('id','numero_visita')
