from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers import UserSerializer, LoginSerializer


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth = {
            'username': serializer.user.username,
            'token': serializer.token
        }
        return Response(auth, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        user.id = pk
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
