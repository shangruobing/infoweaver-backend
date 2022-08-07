from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers import LoginSerializer


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Users login.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth = {
            'username': serializer.user.username,
            'token': serializer.token
        }
        return Response(auth, status=status.HTTP_200_OK)
