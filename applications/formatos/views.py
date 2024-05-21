from django.shortcuts import render

from rest_framework import viewsets
from .models.formatoModels import FormatoPlaneacion
from rest_framework.exceptions import NotFound

from .serializers.formatoSerializer import FormatoSerializer

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