"""Importamos el serializers, para poder trabajar con los json"""
from rest_framework import serializers, pagination

#importamos los modelos
from .models import Ficha, Aprendiz, DocumentacionAprendiz


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

class AprendizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aprendiz
        fields = '__all__'

class FichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = ('id', 'numero_ficha', 'nombre_programa', 'nivel_formacion')



class DocumentacionAprendizSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentacionAprendiz
        fields = '__all__'


class AprendizPagination(pagination.PageNumberPagination):
    page_size = 5
    max_page_size = 50

class FichaPagination(pagination.PageNumberPagination):
    page_size = 3
    max_page_size = 20