"""Importamos el serializers, para poder trabajar con los json"""
from rest_framework import serializers, pagination
from users.serializers import UserSerializer
#importamos los modelos
from django.contrib.auth import get_user_model
from ..models.models import Ficha, Aprendiz, DocumentacionAprendiz, Documentos, Empresa
from ...agendarcitas.serializers.serializers import NumeroVisitaAprendizSerializer, AprendizVisitSerializer

from django.core.mail import send_mail
from django.template.loader import render_to_string
from ..tasks import send_welcome_email

from ...agendarcitas.models.visita import Visita

class ListarFichas(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = '__all__'
        #(
        #     'id',
        #     'nombre_programa',
        #     'numero_ficha',
        #     'aprendices'

        # )

    def create(self, validated_data):
        numero_ficha = validated_data.get('numero_ficha')

        # Verificar si ya existe una ficha con el número proporcionado
        if Ficha.objects.filter(numero_ficha=numero_ficha).exists():
            raise serializers.ValidationError("Ya existe una ficha con este número de ficha.")

        return super().create(validated_data)


#serializador para el modelo empresa
class EmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empresa
        fields = '__all__'



class FichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = ('id', 'numero_ficha', 'nombre_programa', 'nivel_formacion')



User = get_user_model()

class AprendizSerializer(serializers.ModelSerializer):
    visitas = serializers.SerializerMethodField()
    empresa = EmpresaSerializer() 
    ficha = FichaSerializer(read_only=True)
    numero_ficha = serializers.IntegerField(write_only=True)  # Campo para ingresar el número de ficha
   

    # user = UserSerializer(required=False)
    class Meta:
        model = Aprendiz
        fields = '__all__'


    # def validate_numero_ficha(self, value):
    #     try:
    #         ficha = Ficha.objects.get(numero_ficha=value)
    #     except Ficha.DoesNotExist:
    #         raise serializers.ValidationError("El número de ficha no existe")
        
    #     return ficha
    
    def get_visitas(self, obj):
        visitas_del_aprendiz = Visita.objects.filter(aprendiz=obj)  # Obtener las visitas del aprendiz
        numeros_de_visita = visitas_del_aprendiz.values_list('numero_visita', flat=True)
        return list(numeros_de_visita)

    def create(self, validated_data):

        print(validated_data)
        empresa_data = validated_data.pop('empresa')  # Extraer datos de la empresa
        nit = empresa_data.get('nit')
        # Verificar si la empresa ya existe
        empresa, created = Empresa.objects.get_or_create(nit=nit, defaults=empresa_data)
        
        # Asignar la empresa al aprendiz usando la instancia de la empresa
        validated_data['empresa'] = empresa

        numero_ficha = validated_data.pop('numero_ficha')

        # Obtener la instancia de Ficha correspondiente al número de ficha
        try:
            ficha = Ficha.objects.get(numero_ficha=numero_ficha)
        except Ficha.DoesNotExist:
            raise serializers.ValidationError("El número de ficha no existe")

        # Asignar la ficha al aprendiz usando la instancia de Ficha
        validated_data['ficha'] = ficha
       
        
        # Crea el Aprendiz asociado al usuario creado
        aprendiz = Aprendiz.objects.create(**validated_data)
    
        # Establece una contraseña por defecto
        default_password = 'aprendizseep'

        # Extrae los datos relacionados con el usuario del Aprendiz
        user_data = {
            'rol': 'aprendiz',
            'documento': validated_data['numero_documento'],  # Utiliza el número de documento como nombre de usuario
            'password': default_password,  # Utiliza una contraseña por defecto
            'name': validated_data['nombres'],
            'email': validated_data['correo_principal']
        }

        # Crea el usuario asociado al Aprendiz
        user = User.objects.create_user(**user_data)

        # Asigna el usuario creado al aprendiz
        aprendiz.user = user
        aprendiz.save()


       

        # Llamar al método para enviar el correo electrónico
        send_welcome_email(
            email=validated_data['correo_principal'],
            nombres=validated_data['nombres'],
            numero_documento=validated_data['numero_documento'],
            default_password=default_password,
        )


        return aprendiz


# class PerfilAprendiz(serializers.ModelSerializer):

#     class Meta:
#         model = Aprendiz
#         fields = ('id', 'nombres', 'apellidos')


class DocumentacionAprendizSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentacionAprendiz
        fields = '__all__'


#serializador para la documentacion del aprendiz, con registro independiente
        
class DocumentacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Documentos
        fields = '__all__'



class AprendizPagination(pagination.PageNumberPagination):
    page_size = 25
    max_page_size = 50

class FichaPagination(pagination.PageNumberPagination):
    page_size = 3
    max_page_size = 20


#serializers  para listar algunos campos del aprendiz

# class AprendizBasicSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Aprendiz
#         fields = ('nombres', 'apellidos')
    
