from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from ..models import User
from ..pagination import GenericPagination
from ..serializers import UserSerializer


class UserListView(APIView):
    """
    get: user信息
    post: 修改user信息
    """
    authentication_classes = []
    permission_classes = []

    # @method_decorator(cache_page(60 * 60 * 2))
    # @method_decorator(vary_on_headers("Authorization", ))
    def get(self, request, *args, **kwargs):
        """
        Retrieve the registered users.
        """
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        paginator = GenericPagination()
        page_user_list = paginator.paginate_queryset(user_serializer.data,
                                                     self.request, view=self)
        return paginator.get_paginated_response(page_user_list)

    def post(self, request, *args, **kwargs):
        """
        Register a user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    """
    Retrieve, update or delete a user instance.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("NOT_FOUND")

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve a user by ID.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        """
        Update a user by ID.
        """
        user = self.get_object(pk)
        user.id = pk
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete a user by ID.
        """
        user = self.get_object(pk)
        data = {"message": "Successfully Delete",
                "user_id": user.user_id,
                "username": user.username}
        user.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)
