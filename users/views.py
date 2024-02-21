from rest_framework import generics,authentication,permissions
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from users.serializers import UserSerializer, AuthTokenSerializer
from users.models import User, IsAprendiz

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        token_data = serializer.validated_data
        return Response(token_data, status=200)


@permission_classes([IsAprendiz])
class ListarAlgo(ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    def get(self, request ):
        user = request.user

        user_id = user.rol
        return Response({"user_id": user_id})
        # return Response({"mensaje": "Hola mundo"} )