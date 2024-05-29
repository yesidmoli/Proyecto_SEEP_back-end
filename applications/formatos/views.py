from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from .models.formatoModels import FormatoPlaneacion, Seguimiento, Planeacion, Evaluacion
from rest_framework.exceptions import NotFound

from .serializers.formatoSerializer import FormatoSerializer, PlaneacionSerializer, SeguimientoSerializer, EvaluacionSerializer, AprendizCompletoSerializer
from applications.gestionAprendices.models.models import Aprendiz
from applications.gestionAprendices.serializers.serializers import AprendizSerializer

from rest_framework.response import Response
#vista para las solicitudes que se hagan usando la vista viewset para aplicar el crud
class FormatoViewset(viewsets.ModelViewSet):

    # queryset = FormatoPlaneacion.objects.all()
    queryset = None
    serializer_class = FormatoSerializer
     #metodo para listar la documentacion que le pertenece a un aprendiz

    def get_queryset(self):

        queryset = FormatoPlaneacion.objects.all()
        aprendiz_id = self.request.query_params.get('aprendiz_id')  # Obtener el ID del aprendiz desde los parámetros de consulta

        if aprendiz_id:
            queryset = queryset.filter(aprendiz= aprendiz_id)

            if not queryset.exists():  
                raise NotFound("No se encontraron formatos para este aprendiz.")
        return queryset
    
    
    
# class FormatoPlaneacionViewSet(viewsets.ModelViewSet):
#     queryset = FormatoPlaneacion.objects.all()
#     serializer_class = FormatoPlaneacionSerializer
    
#     def get_queryset(self):

#         queryset = FormatoPlaneacion.objects.all()
#         aprendiz_id = self.request.query_params.get('aprendiz_id')  # Obtener el ID del aprendiz desde los parámetros de consulta

#         if aprendiz_id:
#             queryset = queryset.filter(aprendiz= aprendiz_id)

#             if not queryset.exists():  
#                 raise NotFound("No se encontraron formatos para este aprendiz.")
#         return queryset
    

#vista para seguimiento del formato

class PlaneacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = PlaneacionSerializer
    
    def get_queryset(self):

        queryset = Planeacion.objects.all()
        aprendiz_id = self.request.query_params.get('aprendiz_id')  # Obtener el ID del aprendiz desde los parámetros de consulta

        if aprendiz_id:
            queryset = queryset.filter(aprendiz= aprendiz_id)

            if not queryset.exists():  
                raise NotFound("No se encontró planeacion para este aprendiz.")
        return queryset
    
    
class SeguimientoViewSet(viewsets.ModelViewSet):
    queryset = Seguimiento.objects.all()
    serializer_class = SeguimientoSerializer
    
    def get_queryset(self):

        queryset = Seguimiento.objects.all()
        aprendiz_id = self.request.query_params.get('aprendiz_id')  # Obtener el ID del aprendiz desde los parámetros de consulta

        if aprendiz_id:
            queryset = queryset.filter(aprendiz=aprendiz_id)

            if not queryset.exists():  
                raise NotFound("No se encontró seguimiento para este aprendiz.")
        return queryset
    
class EvaluacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    
    def get_queryset(self):

        queryset = Evaluacion.objects.all()
        aprendiz_id = self.request.query_params.get('aprendiz_id')  # Obtener el ID del aprendiz desde los parámetros de consulta

        if aprendiz_id:
            queryset = queryset.filter(aprendiz=aprendiz_id)

            if not queryset.exists():  
                raise NotFound("No se encontró evaluacion para este aprendiz.")
        return queryset
    
    
class FormatoAprendizViewSet(viewsets.ModelViewSet):
    queryset = Aprendiz.objects.all()
    serializer_class = AprendizCompletoSerializer

    @action(detail=False, methods=['get'], url_path='visualizar')
    def visualizar(self, request, *args, **kwargs):
        aprendiz_id = request.query_params.get('aprendiz_id')
        if not aprendiz_id:
            return Response({"error": "aprendiz_id es requerido"}, status=400)

        try:
            aprendiz = Aprendiz.objects.get(id=aprendiz_id)
        except Aprendiz.DoesNotExist:
            raise NotFound("No se encontró el aprendiz.")

        serializer = self.get_serializer(aprendiz)
        return Response(serializer.data)