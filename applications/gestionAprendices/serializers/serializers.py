"""Importamos el serializers, para poder trabajar con los json"""
from rest_framework import serializers, pagination
from users.serializers import UserSerializer
#importamos los modelos
from django.contrib.auth import get_user_model
from ..models.models import Ficha, Aprendiz, DocumentacionAprendiz, Documentos, Empresa, FormularioFinalAprendiz
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

    def update(self, instance, validated_data):
        # Actualizar los campos directos del Aprendiz
        instance.nombres = validated_data.get('nombres', instance.nombres)
        instance.apellidos = validated_data.get('apellidos', instance.apellidos)
        instance.tipo_documento = validated_data.get('tipo_documento', instance.tipo_documento)
        instance.numero_documento = validated_data.get('numero_documento', instance.numero_documento)
        instance.fecha_expedicion = validated_data.get('fecha_expedicion', instance.fecha_expedicion)
        instance.lugar_expedicion = validated_data.get('lugar_expedicion', instance.lugar_expedicion)
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.sexo = validated_data.get('sexo', instance.sexo)
        instance.direccion_domicilio = validated_data.get('direccion_domicilio', instance.direccion_domicilio)
        instance.municipio = validated_data.get('municipio', instance.municipio)
        instance.departamento = validated_data.get('departamento', instance.departamento)
        instance.numero_celular1 = validated_data.get('numero_celular1', instance.numero_celular1)
        instance.numero_celular2 = validated_data.get('numero_celular2', instance.numero_celular2)
        instance.telefono_fijo = validated_data.get('telefono_fijo', instance.telefono_fijo)
        instance.correo_principal = validated_data.get('correo_principal', instance.correo_principal)
        instance.correo_secundario = validated_data.get('correo_secundario', instance.correo_secundario)
        instance.finalizacion_etapa_lectiva = validated_data.get('finalizacion_etapa_lectiva', instance.finalizacion_etapa_lectiva)
        instance.estado_aprobacion = validated_data.get('estado_aprobacion', instance.estado_aprobacion)

        # Actualizar la empresa asociada al aprendiz si se proporciona
        empresa_data = validated_data.get('empresa')
        if empresa_data:
            empresa_serializer = EmpresaSerializer(instance.empresa, data=empresa_data)
            if empresa_serializer.is_valid():
                empresa_serializer.save()
            else:
                raise serializers.ValidationError(empresa_serializer.errors)

        # Actualizar la ficha asociada al aprendiz si se proporciona
        numero_ficha = validated_data.get('numero_ficha')
        if numero_ficha:
            try:
                ficha = Ficha.objects.get(numero_ficha=numero_ficha)
            except Ficha.DoesNotExist:
                raise serializers.ValidationError("La ficha especificada no existe")
            instance.ficha = ficha

        # Guardar los cambios en el objeto Aprendiz
        instance.save()
        return instance
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
    

class FormularioFinalAprendizSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormularioFinalAprendiz
        fields = '__all__'
        