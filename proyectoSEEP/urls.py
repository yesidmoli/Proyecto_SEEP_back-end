
from django.contrib import admin
from django.urls import path, re_path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('applications.gestionAprendices.urls')),
    re_path('', include('applications.agendarcitas.urls')),
    re_path('', include('applications.formatos.urls')),
    re_path('', include('users.urls')),
   
    re_path(r'jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    re_path(r'^jet/', include(('jet.urls', 'jet'), namespace='jet')),  # Django JET URLS corregid
   
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

]
# Agregar la función static() al final de las URLs
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

