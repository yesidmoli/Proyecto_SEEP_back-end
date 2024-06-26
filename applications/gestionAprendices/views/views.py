from django.shortcuts import render
from rest_framework.generics import (ListCreateAPIView, ListAPIView, RetrieveAPIView)
from rest_framework import viewsets
from ..serializers.serializers import *
from ..models.models import Aprendiz, Ficha, Documentos, InstructorEncargado, FormularioFinalAprendiz
from rest_framework.reverse import reverse
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication

from rest_framework.views import APIView

from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from ..filters import AprendizFilter

from rest_framework import generics,authentication,permissions

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

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
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Ficha.objects.all()
    serializer_class = ListarFichas

    def perform_create(self, serializer):

        print("user", self.request.user)
        # Obtener el instructor encargado relacionado con el usuario actual (o el que quieras asignar)
        instructor_encargado = InstructorEncargado.objects.get(user=self.request.user)
        
        # Crear la ficha
        ficha = serializer.save()

        # Agregar el instructor encargado a la ficha
        instructor_encargado.ficha.add(ficha)


        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateBitacoraCheck(APIView):
    def put(self, request, *args, **kwargs):
        aprendiz_id = request.query_params.get('aprendiz_id')
        documentos_actualizados = request.data.get('documentos', [])
        

        if aprendiz_id and documentos_actualizados:
            for documento in documentos_actualizados:
                documento_id = documento.get('id')
                observacion = documento.get('observaciones')

                print("observacion id" , observacion)
                
                is_bitacora_check = documento.get('is_bitacora_check')

                # Obtener el documento y actualizar el check
                try:
                    doc = Documentos.objects.get(pk=documento_id, aprendiz=aprendiz_id)
                    doc.is_bitacora_check = is_bitacora_check
                    doc.observaciones = observacion
                    doc.save()
                except Documentos.DoesNotExist:
                    return Response({"error": f"Documento con id {documento_id} no encontrado para el aprendiz con id {aprendiz_id}"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Checks actualizados correctamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Falta el ID del aprendiz o los documentos actualizados"}, status=status.HTTP_400_BAD_REQUEST)
        
class FormularioFinalView(viewsets.ModelViewSet):
    serializer_class = FormularioFinalAprendizSerializer
    queryset = FormularioFinalAprendiz.objects.all()
    
    

#vista para obtener los aprendices con diferentes estados
@csrf_exempt
def aprendices_certificacion(request):
    if request.method == 'GET':
        try:
            aprobados = Aprendiz.objects.filter(estado_aprobacion='aprobado').count()
            pendientes = Aprendiz.objects.exclude(estado_aprobacion='pendiente').count()

            data = {
                'aprobados': aprobados,
                'pendientes': pendientes,
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
   
@csrf_exempt 

def aprendices_certificacion_por_ficha(request):
    if request.method == 'GET':
        try:
            # Obtener todas las fichas
            todas_las_fichas = Ficha.objects.all()

            # Obtener la cantidad de aprendices aprobados y pendientes por ficha
            data = []
            for ficha in todas_las_fichas:
                aprobados = Aprendiz.objects.filter(ficha=ficha, estado_aprobacion='aprobado').count()
                pendientes = Aprendiz.objects.filter(ficha=ficha).exclude(estado_aprobacion='aprobado').count()

                ficha_data = {
                    'numero_ficha': ficha.numero_ficha,
                    'nombre_programa': ficha.nombre_programa,
                    'nivel_formacion': ficha.nivel_formacion,
                    'horario_formacion': ficha.horario_formacion,
                    'aprobados': aprobados,
                    'pendientes': pendientes,
                }

                data.append(ficha_data)

            return JsonResponse({'fichas': data})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)