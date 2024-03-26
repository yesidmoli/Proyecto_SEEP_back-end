from django.urls import path, include
from dj_rest_auth.views import PasswordResetConfirmView
from .views import *

urlpatterns = [
    
 
    path('api/create-user/', CreateUserView.as_view(), name='create-user'),
    path('api/user-token/', CreateTokenView.as_view(), name='user-token'),
    path('api/update-user/', RetrieveUpdateUserView.as_view(), name='user-token'),
    path('api/listar/', ListarAlgo.as_view(), name='user-token'),

    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),

    path('dj-rest-auth/password/reset/confirm/<slug:uidb64>/<slug:token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    
    
    # path('api/accounts/', include('django.contrib.auth.urls')),




]
