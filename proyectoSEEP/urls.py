
from django.contrib import admin
from django.urls import path, re_path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('applications.gestionAprendices.urls')),
    re_path('', include('applications.agendarcitas.urls')),
    re_path('', include('applications.formatos.urls')),
    re_path('', include('users.urls')),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

]
