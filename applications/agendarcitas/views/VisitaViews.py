from django.shortcuts import render
from rest_framework import viewsets, status

from django.utils import timezone

from users.models import User,  IsInstructor
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from rest_framework.response import Response

from rest_framework.generics import (
    ListCreateAPIView, 
    ListAPIView, 
    RetrieveAPIView,
    CreateAPIView)


from ..serializers.serializers import VisitSerializer, NumeroVisitaAprendizSerializer

from ..models.visita import Visita, InstructorEncargado, Aprendiz

#vista para la creacion de visita, heredando de la vista createApiView
class VisitCreate(CreateAPIView):

    serializer_class = NumeroVisitaAprendizSerializer
    queryset = Visita.objects.all()

#vista para listar las visitas
class VisitList(ListCreateAPIView):

    serializer_class = VisitSerializer
    queryset = Visita.objects.all()


#vista para aplicarle el crud a la visita, heredando de viewset
class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    serializer_class = NumeroVisitaAprendizSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #modificamos el metodo de listar, para listar segun el rol, las visitas
    def list(self, request):

        usuario = request.user
        print("este el el rol", usuario.rol)

        try:
            
            #visitas que le corresponden segun el rol
            if usuario.rol == 'instructor':
                try:
                    instructor_encargado = InstructorEncargado.objects.get(user=usuario)
                    visitas_correspondientes = Visita.objects.filter(instructor_encargado=instructor_encargado , estado = 'programada')
                    serializer = VisitSerializer(visitas_correspondientes, many=True)
                    return Response(serializer.data)
                except InstructorEncargado.DoesNotExist:
                    return Response({"detail": "Perfil de instructor no encontrado"}, status=404)
            
            elif usuario.rol =='aprendiz':

                try:
                    aprendiz = Aprendiz.objects.get(user=usuario)
                    visitas_correspondientes = Visita.objects.filter(aprendiz=aprendiz, estado = 'programada')
                    serializer = VisitSerializer(visitas_correspondientes, many=True)
                    return Response(serializer.data)
                except Aprendiz.DoesNotExist:
                    return Response({"detail": "Perfil de aprendiz no encontrado"}, status=404)

        except InstructorEncargado.DoesNotExist:
             return Response({"detail": "Perfil  no encontrado"}, status=404)

    # def create(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    # def update(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

    # def delete(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


     # Método personalizado para cancelar una visita
    def cancelar_visita(self, request, pk):

        rol = request.user

        if rol.rol == 'instructor':
            try:
                visita = Visita.objects.get(pk=pk)
                if visita.estado == 'programada':
                    motivo_cancelacion = request.data.get('motivo_cancelacion', '')
                    visita.estado = 'cancelada'
                    visita.motivo_cancelacion = motivo_cancelacion  # Asigna el motivo de cancelación
                    visita.fecha_cancelacion = timezone.now()
                    visita.save()
                    return Response({"detail": "Visita cancelada con éxito."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "No se puede cancelar una visita que no está programada."}, status=status.HTTP_400_BAD_REQUEST)
            except Visita.DoesNotExist:
                return Response({"error": "La visita no existe."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Usted no tiene permisos para cancelar una visita"}, status=status.HTTP_400_BAD_REQUEST)

    #metodo para marcar una visita como realizada
    def marcar_realizada(self, request, pk=None):
        visita = self.get_object()
        if visita.estado == 'programada':
            visita.estado = 'realizada'
            visita.save()
            return Response({"detail": "Visita marcada como realizada con éxito."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "La visita no puede marcarse como realizada porque no está programada."}, status=status.HTTP_400_BAD_REQUEST)