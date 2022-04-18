import os
import time

from django.http import FileResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from py2neo import Node, Relationship, Subgraph

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Notice
from .classes.query import graph
from .classes.question import Question
from .filters import NoticeFilterBackend
from .serializers import NoticeSerializer
from .utils.baidu_search import baidu_search
from .classes.pretrained_model import BertModel
from .utils.threads import MultithreadingBert
from .pagination import FileListPagination, NoticePagination
from .utils.state import is_have_history

try:
    model = BertModel()
    print("BERT model loaded successfully")
except RuntimeError:
    print("BERT model load failed")


class TestView(APIView):
    def get(self, request, *args, **kwargs):
        return Response("Welcome Notice File Question & Answer System !", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """测试多轮对话
        1:代表具有历史信息
        """

        state, history = is_have_history(request)
        print(state)
        if state:
            print(history)
            return Response(f"History:{history}", status=status.HTTP_200_OK)
        else:
            return Response("No History", status=status.HTTP_200_OK)


class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        return Response("Welcome Notice File Question & Answer System !", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """上传文件"""
        try:
            # Title = Node("Title", name=request.data["name"])
            # Time = Node("Time", name="Time" + request.data["name"])
            # time = Node("time", name=request.data["data2"])
            # Loc = Node("Location", name="Loc" + request.data["name"])
            # location = Node("location", name=request.data["region"])
            #
            # relation1 = Relationship(Title, "has_time", Time)
            # relation2 = Relationship(Title, "has_location", Loc)
            # relation3 = Relationship(Time, "has_Time", time)
            # relation4 = Relationship(Loc, "location", location)
            #
            # node_ls = [Title, Time, Loc, time, location]
            # relation_ls = [relation1, relation2, relation3, relation4]
            # subgraph = Subgraph(node_ls, relation_ls)
            # tx = graph.begin()
            # tx.create(subgraph)
            # graph.commit(tx)

            file = request.FILES.get('file')
            default_storage.save(rf"./upload/{file.name}", content=ContentFile(file.read()))
            return Response(f'{file.name} upload OK')
        except AttributeError:
            return Response('upload ERROR', status=status.HTTP_400_BAD_REQUEST)


class NoticeListView(APIView):

    def get(self, request, *args, **kwargs):
        """
        查询通知文件
        如果没有指定条件，默认返回分页后的所有文件
        可以通过 ?name&start_date&end_date 在URL中指出条件
        """
        notices = Notice.objects.all()
        notice_filter = NoticeFilterBackend()
        notices = notice_filter.filter_queryset(request, notices, view=self)
        serializer = NoticeSerializer(notices, many=True, context={'request': request})
        paginator = FileListPagination()
        page_user_list = paginator.paginate_queryset(serializer.data, self.request, view=self)
        return paginator.get_paginated_response(page_user_list)

    def post(self, request, *args, **kwargs):
        """
        通过发送POST请求,将位于Neo4j中的文件结点批量插入MySQL数据库
        """
        query = "MATCH (n:Title)-[*2]-(t:abstract) RETURN n,id(n),collect(t.name)"
        result = graph.run(query).data()
        neoFileName = []
        neoFileId = []

        for i in result:
            neoFileName.append(i["n"]["name"])
            neoFileId.append(i["id(n)"])

        filePath = r"..\public\Word"  # 文件夹路径

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
        根据id查询单个通知文件
        """
        notices = self.get_object(pk)
        serializer = NoticeSerializer(notices, context={'request': request})
        file_path = "..\\public\\Word\\" + serializer.data['name']
        return FileResponse(open(file_path, 'rb'))


class Neo4jView(APIView):
    def get(self, request, pk, *args, **kwargs):
        """
        根据图数据库中的文件id查询这个文件的标题
        本方法是测试数据库连通性时候使用
        :param request: 请求
        :param pk: 文件ID
        """
        cypher = f"match (n:Title)-[*2]-(t:abstract) where id(n)={pk} unwind t.name as answer return answer"
        answer = graph.run(cypher).data()
        result = [i['answer'] for i in answer]
        return Response(result)

    def post(self, request, *args, **kwargs):
        """
        本方法是问答机器人的主方法
        通过文件名匹配->Neo4j->百度百科的顺序依次进行查询
        """
        question = request.data['question']
        print("request", request.data)
        state, history = is_have_history(request)

        if state:
            file_id = history.get('file_id', '')
            cypher = f"match (title)-[]-(context:File) where id(title)={file_id} return context.name"
            context = graph.run(cypher).data()[0].get("context.name", "")
            context = ''.join(context.split()).strip()
            result = MultithreadingBert(model, question, context, thread_number=8).run_threads()
            return Response({"results": result})

        else:
            question_object = Question(question)
            notices = question_object.get_query_results()

        serializer = NoticeSerializer(notices, many=True, context={'request': request})
        if len(serializer.data) == 0:
            # print("Neo4查询失败 百度百科查询")
            return Response({"results": baidu_search(question)})

        paginator = NoticePagination()
        page_user_list = paginator.paginate_queryset(serializer.data, self.request, view=self)
        return paginator.get_paginated_response(page_user_list)

    def put(self, request, *args, **kwargs):
        """
        根据file_id查询文件内容 并输入BERT取得结果
        试验阶段只能通过postman测试
        性能捉急!!!
        2k字     15s
        500字    2-3s
        100字    0.3s
        """
        try:
            question = request.data['question']
            file_id = request.data['id']

            thread_number = int(request.data['thread'])

            cypher = f"match (title)-[]-(context:File) where id(title)={file_id} return context.name"

            context = graph.run(cypher).data()[0].get("context.name", "")
            context = ''.join(context.split()).strip()
            if thread_number > 1:
                result = MultithreadingBert(model, question, context, thread_number).run_threads()
            else:
                result = model.fit(question, context)

            return Response(result)
        except (IndexError, KeyError):
            return Response('ERROR!', status=status.HTTP_400_BAD_REQUEST)
