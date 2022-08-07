from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..utils.system_info import get_system_info


class HomeView(APIView):
    """
    Welcome to Infoweaver Question & Answer System.
    """
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return Response({'info': "Welcome to Infoweaver Question & Answer System."}, status=status.HTTP_200_OK)


class APIHomeView(APIView):
    """
    Welcome to Infoweaver API.
    """
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return Response({'info': "Welcome to Infoweaver Application Program Interface."}, status=status.HTTP_200_OK)


class SystemView(APIView):
    """
    Retrieve server information.
    """

    def get(self, request, *args, **kwargs):
        return Response(get_system_info(), status=status.HTTP_200_OK)
