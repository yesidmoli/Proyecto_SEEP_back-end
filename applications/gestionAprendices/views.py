from django.shortcuts import render
from rest_framework.generics import (ListCreateAPIView, ListAPIView, RetrieveAPIView)
from rest_framework import viewsets
from .serializers import *
from .models import Aprendiz, Ficha
from rest_framework.reverse import reverse


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from .filters import AprendizFilter


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
    
class AprendizListView(ListAPIView):
    serializer_class = AprendizSerializer
    queryset = Aprendiz.objects.all()

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = AprendizFilter 

    pagination_class = AprendizPagination


class DocumentacionAprendizViewSet(viewsets.ModelViewSet):
    queryset = DocumentacionAprendiz.objects.all()
    serializer_class = DocumentacionAprendizSerializer


#creacion de ficha
class CrearFichaViewset(viewsets.ModelViewSet):
    queryset = Ficha.objects.all()
    serializer_class = ListarFichas