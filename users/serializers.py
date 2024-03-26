from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from applications.gestionAprendices.models.models import InstructorEncargado, Aprendiz
from applications.gestionAprendices.serializers.InstructoSerializer import InstructorSerializer
from applications.gestionAprendices.serializers.AprendizSerializer import PerfilAprendiz
from rest_framework.response import Response

from django.contrib.auth.forms import PasswordResetForm
from dj_rest_auth.serializers import PasswordResetSerializer

from .forms import CustomResetForm

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['rol','documento', 'password', 'name']
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validate_data):
        return get_user_model().objects.create_user(**validate_data)
    
    def update(self, intance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(intance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
    
class AuthTokenSerializer(serializers.Serializer):
    rol = serializers.CharField()
    documento = serializers.CharField()
    password = serializers.CharField(style={'input_type':'password'})

    def validate(self, data):
        rol = data.get('rol')
        documento = data.get('documento')
        password = data.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=documento,
            password=password,
            rol = rol
        )

        if not user:
            raise serializers.ValidationError('No se pudo autenticar', code='authorization')
        
        # Si el usuario se autentica correctamente, verificar el rol adicionalmente
        if rol != user.rol:
            msg = 'El rol proporcionado no coincide con el rol del usuario.'
            raise serializers.ValidationError(msg, code='invalid')
        
        # data['user'] = user
        # return data
        # Obtén o crea el token de autenticación para el usuario
        token, _ = Token.objects.get_or_create(user=user)
        
        # Obtén el perfil de usuario asociado (si existe)
        try:
            rol = user.rol
            if rol == 'instructor':

                user_profile = InstructorEncargado.objects.get(user=user)
                # Serializa los datos del perfil de usuario
                user_profile_data = InstructorSerializer(user_profile).data
            elif rol == 'aprendiz':
                user_profile = Aprendiz.objects.get(user=user)
                # Serializa los datos del perfil de usuario
                user_profile_data = PerfilAprendiz(user_profile).data

        except Aprendiz.DoesNotExist:
           
            user_profile_data = None
            return {"error": "No se encontró un perfil de aprendiz asociado."}
        except InstructorEncargado.DoesNotExist:
           
            user_profile_data = None
            return {"error": "No se encontró un perfil de instructor asociado."}

        return  {'token': token.key, 'rol': rol, 'user_profile': user_profile_data}
    

    def create(self, validated_data):
        raise NotImplementedError('`create()` method is not implemented')
    

class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomResetForm