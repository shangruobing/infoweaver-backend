from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notice
import os
from django.http import FileResponse, StreamingHttpResponse
from .serializers import NoticeSerializer
from .pagination import MyPagination
from .filters import NoticeFilterBackend
import time
from rest_framework import status
from rest_framework.exceptions import APIException
from py2neo import Graph, Node, Relationship
import py2neo
import jieba
import jieba.posseg as pseg

jieba.enable_paddle()


class NoticeListView(APIView):

    def get(self, request, *args, **kwargs):
        notices = Notice.objects.all()
        notice_filter = NoticeFilterBackend()
        notices = notice_filter.filter_queryset(request, notices, view=self)
        serializer = NoticeSerializer(notices, many=True, context={'request': request})
        paginator = MyPagination()
        page_user_list = paginator.paginate_queryset(serializer.data, self.request, view=self)
        return paginator.get_paginated_response(page_user_list)

    def post(self, request, *args, **kwargs):
        """将文件批量插入数据库"""
        graph = Graph("http://localhost:7474", auth=("neo4j", "010209"))
        query = "MATCH (n:Title) RETURN n,id(n)"
        result = graph.run(query).data()
        neoFileName = []
        neoFileId = []
        for i in result:
            neoFileName.append(i["n"]["name"])
            neoFileId.append(i["id(n)"])

        try:
            filePath = r"C:\Users\冰\Desktop\NFQA后端开发\public\Word"  # 文件夹路径

            for i, file in enumerate(neoFileName):
                filename = neoFileName[i] + ".docx"
                mtime = os.stat(os.path.join(filePath, filename)).st_mtime
                file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                Notice(name=filename, date=file_modify_time, file_id=neoFileId[i]).save()
            return Response("Word文件信息已经成功导入Mysql")
        except Exception:
            return Response("Word文件信息录入错误 可能是由于主键重复", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NoticeView(APIView):
    def get_object(self, pk):
        try:
            return Notice.objects.get(pk=pk)
        except Notice.DoesNotExist:
            raise NotFound("NOT_FOUND")

    def get(self, request, pk, *args, **kwargs):
        notices = self.get_object(pk)
        serializer = NoticeSerializer(notices, context={'request': request})
        file_path = "C:\\Users\\冰\\Desktop\\NFQA后端开发\\public\\Word\\" + serializer.data['name']
        return FileResponse(open(file_path, 'rb'))
        # return StreamingHttpResponse(open(file_path, 'rb'))


class Neo4jView(APIView):

    def post(self, request, *args, **kwargs):
        print("request", request.data)
        question = request.data['question']
        # 词性标注
        question_type = None
        answer_type = None
        words = pseg.cut(question, use_paddle=True)

        cypher = ""
        for word, flag in words:
            print(word, flag)
            question = word
            if flag == 'TIME':
                question_type = 'time'
                cypher = f'match(n:{question_type})-[*2]-(answer:Title) where n.name contains "{question}" return answer,id(answer)'
            if flag == 'LOC':
                question_type = 'location'
                cypher = f'match(n:{question_type})-[*2]-(answer:Title) where n.name contains "{question}" return answer,id(answer)'
            if flag == 'ORG':
                question_type = 'org'
                cypher = f'match(n:{question_type})-[*2]-(answer:Title) where n.name contains "{question}" return answer,id(answer)'
            if flag == 'PER':
                question_type = 'person'
                cypher = f'match(n:{question_type})-[*2]-(answer:Title) where n.name contains "{question}" return answer,id(answer)'

        try:
            graph = Graph("http://localhost:7474", auth=("neo4j", "010209"))
        except py2neo.errors.ConnectionUnavailable:
            raise APIException("Neo4j Connection Unavailable", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        answer = graph.run(cypher).data()
        print('cypher:', cypher)
        print('answer', answer)

        id_list = [i['id(answer)'] for i in answer]

        print("ID List", id_list)
        notices = Notice.objects.filter(file_id__in=id_list)
        print("Notices", notices)
        serializer = NoticeSerializer(notices, many=True, context={'request': request})
        # print("serializer data", serializer.data)
        paginator = MyPagination()
        page_user_list = paginator.paginate_queryset(serializer.data, self.request, view=self)
        return paginator.get_paginated_response(page_user_list)
