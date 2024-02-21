from django.urls import path, include

from .views import *

urlpatterns = [
    
 
    path('api/create-user/', CreateUserView.as_view(), name='create-user'),
    path('api/user-token/', CreateTokenView.as_view(), name='user-token'),
    path('api/update-user/', RetrieveUpdateUserView.as_view(), name='user-token'),
    path('api/listar/', ListarAlgo.as_view(), name='user-token'),


]
