import os
import shutil

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from ..models import UploadFile
from ..classes.file_convertor import Docx2txt
from ..pagination import UploadFilePagination
from ..serializers import UploadFileSerializer
from ..classes.graph_loader import Neo4jDataLoader


class UploadFileListView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Retrieve the uploaded File.
        """
        files = UploadFile.objects.all()
        file_serializer = UploadFileSerializer(files, many=True)
        paginator = UploadFilePagination()
        page_user_list = paginator.paginate_queryset(file_serializer.data, self.request, view=self)
        return paginator.get_paginated_response(page_user_list)

    def post(self, request, *args, **kwargs):
        """
        Upload a File.
        """
        try:
            file = request.FILES.get('file')
            username = request.data.get("username")
            file_name = file.name
            data = {
                "file_name": file_name,
                "username": username
            }
            serializer = UploadFileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            default_storage.save(f"{settings.MEDIA_ROOT}/upload/{file.name}", content=ContentFile(file.read()))
            return Response(f'{file.name} upload OK')
        except AttributeError:
            return Response('Upload ERROR', status=status.HTTP_400_BAD_REQUEST)

    def options(self, request, *args, **kwargs):
        """
        File Operation Commands.
        """
        file_path = settings.MEDIA_ROOT + "/upload/"
        target_path = settings.MEDIA_ROOT + "/temp/docx/"
        self.move_files(file_path, target_path)

        txt_path = settings.MEDIA_ROOT + "/temp/txt/"
        Docx2txt(target_path, txt_path).execute_file_convert()
        Neo4jDataLoader(txt_path).execute_load()
        self.clear_table()

        shutil.rmtree(settings.MEDIA_ROOT + "/upload/", True)
        os.mkdir(settings.MEDIA_ROOT + "/upload/")
        return Response("Testing...")

    @staticmethod
    def clear_table():
        UploadFile.objects.all().delete()

    def move_files(self, file_path, target_path):
        file_list = os.listdir(file_path)
        for file in file_list:
            shutil.move(file_path + file, target_path)


class UploadFileView(APIView):

    @staticmethod
    def get_object(pk):
        try:
            return UploadFile.objects.get(pk=pk)
        except UploadFile.DoesNotExist:
            raise NotFound("NOT_FOUND")

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve an uploaded file by ID.
        """
        file = self.get_object(pk)
        serializer = UploadFileSerializer(file)
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete an uploaded file by ID.
        """
        file = self.get_object(pk)
        file.delete()
        default_storage.delete(f"{settings.MEDIA_ROOT}/upload/{file.file_name}")
        return Response(f'{file.file_name} delete OK')
