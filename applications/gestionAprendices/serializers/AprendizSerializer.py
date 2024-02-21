from rest_framework import serializers
from ..models.models import  Aprendiz

class PerfilAprendiz(serializers.ModelSerializer):

    class Meta:
        model = Aprendiz
        fields = ('id', 'nombres', 'apellidos','numero_documento' , 'correo_principal', 'numero_celular1', 'user' )
