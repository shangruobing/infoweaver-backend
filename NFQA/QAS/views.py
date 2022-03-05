from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notice
import os
from django.http import FileResponse
from .serializers import NoticeSerializer
from .pagination import MyPagination
from .filters import NoticeFilterBackend
import time
from rest_framework import status
from rest_framework.exceptions import APIException
from py2neo import Graph
import py2neo
import jieba
import jieba.posseg as pseg

jieba.enable_paddle()
# 挂载全局图数据库实例
try:
    graph = Graph("http://localhost:7474", auth=("neo4j", "010209"))
except py2neo.errors.ConnectionUnavailable:
    # raise APIException("Neo4j Connection Unavailable", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    print(APIException("Neo4j Connection Unavailable", code=status.HTTP_500_INTERNAL_SERVER_ERROR))


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

        query = "MATCH (n:Title)-[*2]-(t:abstract) RETURN n,id(n),collect(t.name)"
        result = graph.run(query).data()
        neoFileName = []
        neoFileId = []
        # neoContent = []
        for i in result:
            neoFileName.append(i["n"]["name"])
            neoFileId.append(i["id(n)"])
            # neoContent.append(i["collect(t.name)"])

        filePath = r"C:\Users\冰\Desktop\NFQA后端开发\public\Word"  # 文件夹路径

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
        notices = self.get_object(pk)
        serializer = NoticeSerializer(notices, context={'request': request})
        file_path = "C:\\Users\\冰\\Desktop\\NFQA后端开发\\public\\Word\\" + serializer.data['name']
        return FileResponse(open(file_path, 'rb'))


class Neo4jView(APIView):
    def get(self, request, pk, *args, **kwargs):
        cypher = f"match (n:Title)-[*2]-(t:abstract) where id(n)={pk} unwind t.name as answer return answer"
        answer = graph.run(cypher).data()
        result = [i['answer'] for i in answer]
        return Response(result)

    def post(self, request, *args, **kwargs):
        print("request", request.data)
        question = request.data['question']
        # 词性标注
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

        answer = graph.run(cypher).data()
        print('cypher:', cypher)
        print('answer', answer)

        id_list = [i['id(answer)'] for i in answer]

        print("ID List", id_list)
        notices = Notice.objects.filter(file_id__in=id_list)
        print("Notices", notices)
        serializer = NoticeSerializer(notices, many=True, context={'request': request})
        paginator = MyPagination()
        page_user_list = paginator.paginate_queryset(serializer.data, self.request, view=self)
        return paginator.get_paginated_response(page_user_list)
