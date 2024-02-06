from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from .views import FichaListView, AprendizListView, DocumentacionAprendizViewSet, CrearFichaViewset

app_name = 'aprendices_app'

router = DefaultRouter()
router.register(r'documentacion-aprendiz', DocumentacionAprendizViewSet, basename='documentacion-aprendiz')
router.register(r'fichas', CrearFichaViewset, basename='ficha')
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/fichas-list/', FichaListView.as_view(), name='ficha-list'),
    path('api/aprendices/', AprendizListView.as_view(), name='aprendices-list'),
]
# Configuración de archivos estáticos y multimedia para desarrollo
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


