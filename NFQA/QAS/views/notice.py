import os
import time

from django.conf import settings
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from ..models import Notice
from ..classes.query import graph
from ..filters import NoticeFilterBackend
from ..pagination import GenericPagination
from ..serializers import NoticeSerializer


class NoticeListView(APIView):

    def get(self, request, *args, **kwargs):
        """
        Retrieve the Notification Files.
        If no condition is specified, all files after paging are returned by default.
        Can pass ?name&start_date&end_date indicates the condition in the URL.
        """
        notices = Notice.objects.all()
        notice_filter = NoticeFilterBackend()
        notices = notice_filter.filter_queryset(request, notices, view=self)
        serializer = NoticeSerializer(notices, many=True, context={'request': request})
        paginator = GenericPagination()
        page_user_list = paginator.paginate_queryset(serializer.data, self.request, view=self)
        return paginator.get_paginated_response(page_user_list)

    def post(self, request, *args, **kwargs):
        """
        Batch insert file nodes located in Neo4j into MySQL database.
        """
        query = "MATCH (n:Title)-[*2]-(t:abstract) RETURN n,id(n),collect(t.name)"
        result = graph.run(query).data()
        neoFileName = []
        neoFileId = []

        for i in result:
            neoFileName.append(i["n"]["name"])
            neoFileId.append(i["id(n)"])

        filePath = settings.MEDIA_ROOT + "/files/docx/"

        for i, file in enumerate(neoFileName):
            try:
                filename = neoFileName[i] + ".docx"
                mtime = os.stat(os.path.join(filePath, filename)).st_mtime
                file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                Notice(name=filename, date=file_modify_time, file_id=neoFileId[i]).save()
            except Exception as e:
                print(e)
                continue

        return Response("Word文件信息导入MySQL完成 但可能存在错误 需要在Django端查看")


class NoticeView(APIView):
    def get_object(self, pk):
        try:
            return Notice.objects.get(pk=pk)
        except Notice.DoesNotExist:
            raise NotFound("NOT_FOUND")

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve a notification file by ID.
        """
        notices = self.get_object(pk)
        serializer = NoticeSerializer(notices, context={'request': request})
        file_path = settings.MEDIA_ROOT + "/files/docx/" + serializer.data['name']
        return FileResponse(open(file_path, 'rb'))
