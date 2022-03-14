from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notice
import os
from django.http import FileResponse
from .serializers import NoticeSerializer
from .pagination import FileListPagination, NoticePagination
from .filters import NoticeFilterBackend
import time
from rest_framework import status
from rest_framework.exceptions import APIException
from py2neo import Graph
import py2neo
import jieba
import jieba.posseg as pseg
import difflib

# 加载字典
try:
    with open(r'C:\Users\冰\Desktop\NFQA后端开发\public\mydict.txt', encoding='UTF-8') as dict_file:
        myDict = dict_file.readlines()
        print("Custom file dictionary loaded successfully")
except Exception:
    raise APIException("Custom file dictionary loading failed")

try:
    jieba.enable_paddle()
except Exception:
    raise APIException("Paddle loading failed")

try:
    graph = Graph("http://localhost:7474", auth=("neo4j", "010209"))
    print("Neo4j graph database connection succeeded")
except py2neo.errors.ConnectionUnavailable:
    raise APIException("Neo4j graph database connection failed", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # print(APIException("Neo4j Connection Unavailable", code=status.HTTP_500_INTERNAL_SERVER_ERROR))


class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        return Response("Welcome Notice File Question & Answer System !", status=status.HTTP_200_OK)


class NoticeListView(APIView):

    def get(self, request, *args, **kwargs):
        notices = Notice.objects.all()
        notice_filter = NoticeFilterBackend()
        notices = notice_filter.filter_queryset(request, notices, view=self)
        serializer = NoticeSerializer(notices, many=True, context={'request': request})
        paginator = FileListPagination()
        page_user_list = paginator.paginate_queryset(serializer.data, self.request, view=self)
        return paginator.get_paginated_response(page_user_list)

    def post(self, request, *args, **kwargs):
        """将文件批量插入数据库"""

        query = "MATCH (n:Title)-[*2]-(t:abstract) RETURN n,id(n),collect(t.name)"
        result = graph.run(query).data()
        neoFileName = []
        neoFileId = []

        for i in result:
            neoFileName.append(i["n"]["name"])
            neoFileId.append(i["id(n)"])

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

        dictResult = difflib.get_close_matches(question, myDict, 1, cutoff=0.6)
        if dictResult:
            notices = Notice.objects.filter(name__icontains=dictResult[0][:-5])
            print("question存在自定义字典")
            print(notices)
        else:
            print("进行Neo4j查询")
            id_list = self.__execute_cypher_query(question)
            notices = Notice.objects.filter(file_id__in=id_list)

        serializer = NoticeSerializer(notices, many=True, context={'request': request})
        paginator = NoticePagination()
        page_user_list = paginator.paginate_queryset(serializer.data, self.request, view=self)
        return paginator.get_paginated_response(page_user_list)

    def __get_cypher(self, condition: []) -> str:
        cypher = ""
        if len(condition) == 1:
            cypher = f'match(n:{condition[0]["question_type"]})-[*2]-(answer:Title) where n.name contains "{condition[0]["question"]}" return answer,id(answer)'
        elif len(condition) == 2:
            cypher = f'match(n:{condition[0]["question_type"]})-[*2]-(answer:Title) where n.name contains "{condition[0]["question"]}" with answer match (answer)-[*2]-(s:{condition[1]["question_type"]}) where s.name contains "{condition[1]["question"]}" return answer,id(answer)'
        elif len(condition) == 3:
            cypher = f'match(n:{condition[0]["question_type"]})-[*2]-(answer:Title) where n.name contains "{condition[0]["question"]}" with answer match (answer)-[*2]-(s:{condition[1]["question_type"]}) where s.name contains "{condition[1]["question"]}" with answer match (answer)-[*2]-(c:{condition[2]["question_type"]}) where c.name contains "{condition[2]["question"]}" return answer,id(answer)'
        elif len(condition) == 4:
            cypher = f'match(n:{condition[0]["question_type"]})-[*2]-(answer:Title) where n.name contains "{condition[0]["question"]}" with answer match (answer)-[*2]-(s:{condition[1]["question_type"]}) where s.name contains "{condition[1]["question"]}" with answer match (answer)-[*2]-(c:{condition[2]["question_type"]}) where c.name contains "{condition[2]["question"]}" with answer match (answer)-[*2]-(d:{condition[3]["question_type"]}) where d.name contains "{condition[3]["question"]}" return answer,id(answer)'
        return cypher

    def __execute_cypher_query(self, question: str) -> []:
        """输入条件列表 输出查询到的文件ID列表"""
        words = pseg.cut(question, use_paddle=True)
        condition = []
        nodes_label = {
            "TIME": "time",
            "LOC": "location",
            "ORG": "org",
            "PER": "person"
        }
        print("Paddle 词性标注结果")
        for question, flag in words:
            print(question, flag)
            try:
                condition.append({'question_type': nodes_label[flag], 'question': question})
            except KeyError as e:
                print(e)
                continue

        cypher = self.__get_cypher(condition)
        answer = graph.run(cypher).data()
        id_list = [i['id(answer)'] for i in answer]
        return id_list
