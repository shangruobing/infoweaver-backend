from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..utils.system_info import get_system_info


class HomeView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return Response({'info': "Welcome Infoweaver Question & Answer System !"}, status=status.HTTP_200_OK)


class APIHomeView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return Response({'info': "Welcome Infoweaver Application Program Interface!"}, status=status.HTTP_200_OK)


class SystemView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(get_system_info(), status=status.HTTP_200_OK)
