from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from ..utils.system_info import get_system_info


class HomeView(APIView):
    """
    Welcome to Infoweaver Question & Answer System.
    """
    authentication_classes = []

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        return Response({'info': "Welcome to Infoweaver Question & Answer System."}, status=status.HTTP_200_OK)


class APIHomeView(APIView):
    """
    Welcome to Infoweaver API.
    """
    authentication_classes = []

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        return Response({'info': "Welcome to Infoweaver Application Program Interface."}, status=status.HTTP_200_OK)


class SystemView(APIView):
    """
    Retrieve server information.
    """

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        return Response(get_system_info(), status=status.HTTP_200_OK)
