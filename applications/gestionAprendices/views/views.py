from django.shortcuts import render
from rest_framework.generics import (ListCreateAPIView, ListAPIView, RetrieveAPIView)
from rest_framework import viewsets
from ..serializers.serializers import *
from ..models.models import Aprendiz, Ficha, Documentos, InstructorEncargado
from rest_framework.reverse import reverse
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from ..filters import AprendizFilter


class FichaListView(ListAPIView):
    queryset = Ficha.objects.all()
    serializer_class = FichaSerializer



"""class AprendizListView(ListAPIView):
    serializer_class = AprendizSerializer

    def get_queryset(self):
        numero_ficha = self.request.query_params.get('ficha', None)
        if numero_ficha is not None:
            return Aprendiz.objects.filter(fichas__numero_ficha=numero_ficha)
        return Aprendiz.objects.none()  # Devolver una consulta vacía si no se proporciona 'ficha'"""
    
class AprendizListView(viewsets.ModelViewSet):
    serializer_class = AprendizSerializer
    queryset = Aprendiz.objects.all()

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = AprendizFilter 

    pagination_class = AprendizPagination


    




# class AprendizDatosView(ListAPIView):
#     serializer_class = AprendizSerializer

#     def detalle_aprendiz(request, id):
        
#         aprendiz = Aprendiz.objects.get(id=id)
#         visitas_aprendiz = aprendiz.visita_set.all()
        

#         #serializamos las visitas
#         serializer = 



# class DocumentacionAprendizViewSet(viewsets.ModelViewSet):
#     queryset = DocumentacionAprendiz.objects.all()
#     serializer_class = DocumentacionAprendizSerializer



#vista para la creacion de registros de los documentos del aprendiz, por separado

class DocumentacionAprendizViewSet(viewsets.ModelViewSet):


    serializer_class = DocumentacionSerializer

    #metodo para listar la documentacion que le pertenece a un aprendiz

    def get_queryset(self):

        queryset = Documentos.objects.all()
        aprendiz_id = self.request.query_params.get('aprendiz_id')  # Obtener el ID del aprendiz desde los parámetros de consulta

        if aprendiz_id:
            queryset = queryset.filter(aprendiz= aprendiz_id)
            return queryset


#creacion de ficha
class CrearFichaViewset(viewsets.ModelViewSet):
    queryset = Ficha.objects.all()
    serializer_class = ListarFichas