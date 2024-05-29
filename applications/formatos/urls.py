from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import FormatoAprendizViewSet

# Crea un enrutador
router = DefaultRouter()

# Registra tu viewset con el enrutador
# router.register('formato', views.FormatoViewset,  basename='formato')
router.register('planeacion', views.PlaneacionViewSet,  basename='planeacion')
router.register('seguimiento', views.SeguimientoViewSet,  basename='seguimiento')
router.register('evaluacion', views.EvaluacionViewSet,  basename='evaluacion')

# Si tienes más viewsets, puedes registrarlos aquí
# router.register('nombre-modelo', views.NombreModeloViewSet)

# Define tus rutas URL incluyendo las rutas del enrutador
urlpatterns = [
    # Opcional: puedes agregar otras vistas basadas en funciones o clases aquí si es necesario
    # path('otra-ruta/', views.otra_vista, name='nombre_vista'),
    path('api/formato/', include(router.urls)),
    path('api/formato/visualizar/', FormatoAprendizViewSet.as_view({'get': 'visualizar'}), name='formar_aprendiz'),
    
]
