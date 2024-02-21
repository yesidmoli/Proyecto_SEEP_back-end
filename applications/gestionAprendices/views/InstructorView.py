from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework import generics,authentication,permissions

from rest_framework.response import Response

from rest_framework.generics import ListAPIView
from ..models.models import InstructorEncargado
from ..serializers.InstructoSerializer import InstructorSerializer
from users.models import User,  IsInstructor

from ..models.models import InstructorEncargado, Ficha, Aprendiz
from ..serializers.serializers import FichaSerializer
from ..serializers.AprendizSerializer import PerfilAprendiz

class InstructorViewSet(viewsets.ModelViewSet):

    serializer_class = InstructorSerializer
    queryset = InstructorEncargado.objects.all()

@permission_classes([IsInstructor])
class ListaFichasCargo(ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):

        usuario = request.user

        #obtenemos el perfil, del intructor encargado
        try:
            instructor_encargado = InstructorEncargado.objects.get(user= usuario)

        except InstructorEncargado.DoesNotExist:
             return Response({"detail": "Perfil de instructor encargado no encontrado"}, status=404)


        fichas_asociadas = instructor_encargado.ficha.all()
        
        # Serializar las fichas
        serializer = FichaSerializer(fichas_asociadas, many=True)

        return Response(serializer.data)
    
@permission_classes([IsInstructor])
class AprendicesInstructorEcargado(ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):

        usuario = request.user

        #obtenemos el perfil, del intructor encargado
        try:
            instructor_encargado = InstructorEncargado.objects.get(user= usuario)

        except InstructorEncargado.DoesNotExist:
             return Response({"detail": "Perfil de instructor encargado no encontrado"}, status=404)
    

        aprendices_del_instructor = Aprendiz.objects.filter(ficha__in=instructor_encargado.ficha.all())

        serializer = PerfilAprendiz(aprendices_del_instructor , many= True)

        return Response(serializer.data)