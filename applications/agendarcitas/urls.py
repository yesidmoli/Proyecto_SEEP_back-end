from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import VisitCreate, VisitList, VisitViewSet

# Configura el enrutador para las vistas del modelo
router = DefaultRouter()
router.register(r'visit', VisitViewSet)

"""urlpatterns = [
    path('api/create-visit/', VisitCreate.as_view(), name='create-visit'),
    path('api/create-visit-list/', VisitList.as_view(), name='create-visit-list'),
    path('api/visit/<int:pk>/cancel/', VisitViewSet.as_view({'delete': 'cancelar_visita'}), name='cancelar-visita'),
    path('api/visit/<int:pk>/marcar-realizada/', VisitViewSet.as_view({'post': 'marcar_realizada'}), name='marcar-realizada'),
]

urlpatterns += router.urls"""  # Agrega las URL generadas por el enrutador al final 

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/create-visit/', VisitCreate.as_view(), name='create-visit'),
    path('api/create-visit-list/', VisitList.as_view(), name='create-visit-list'),
    path('api/visit/<int:pk>/cancel/', VisitViewSet.as_view({'post': 'cancelar_visita'}), name='cancelar-visita'),
    path('api/visit/<int:pk>/marcar-realizada/', VisitViewSet.as_view({'post': 'marcar_realizada'}), name='marcar-realizada'),
]