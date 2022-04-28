import os
import time
import shutil

from django.conf import settings
from django.http import FileResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .classes.query import graph
from .models import Notice, UploadFile
from .classes.question import Question
from .filters import NoticeFilterBackend
from .classes.file_convertor import Docx2txt

from .utils import answer_type
from .utils.threads import MultithreadingBert
from .utils.system_info import get_system_info
from .classes.pretrained_model import BertModel
from .classes.Neo4jDataLoader import Neo4jDataLoader
from .serializers import NoticeSerializer, UploadFileSerializer
from .pagination import FileListPagination, NoticePagination, UploadFilePagination

try:
    model = BertModel()
    print("BERT model loaded successfully")
except RuntimeError:
    raise Exception("BERT model load failed")


class SystemView(APIView):
    def get(self, request, *args, **kwargs):
        xx = get_system_info()
        return Response(xx, status=status.HTTP_200_OK)


class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        return Response("Welcome Notice File Question & Answer System !", status=status.HTTP_200_OK)


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
        根据id查询单个通知文件
        """
        notices = self.get_object(pk)
        serializer = NoticeSerializer(notices, context={'request': request})
        file_path = settings.MEDIA_ROOT + "/files/docx/" + serializer.data['name']
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

        has_history = request.data.get('has_history', False)

        if has_history:
            history = request.data.get('history')
            file_id = history.get('file_id', '')
            cypher = f"match (title)-[]-(context:File) where id(title)={file_id} return context.name"
            context = graph.run(cypher).data()[0].get("context.name", "")
            context = ''.join(context.split()).strip()
            result = MultithreadingBert(model, question, context, thread_number=8).run_threads()
            return Response({"answer_type": answer_type.BERT, "results": result})

        else:
            question_object = Question(question)
            result_type, result = question_object.get_query_results()

            if result_type in (answer_type.DATABASE, answer_type.LOCAL):
                serializer = NoticeSerializer(result, many=True, context={'request': request})
                paginator = NoticePagination()
                page_user_list = paginator.paginate_queryset(serializer.data, self.request, view=self)
                return paginator.get_paginated_response(page_user_list)

            else:
                return Response({"answer_type": result_type, "results": result})

    def put(self, request, *args, **kwargs):

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


class UploadFileListView(APIView):
    def get(self, request, *args, **kwargs):
        files = UploadFile.objects.all()
        file_serializer = UploadFileSerializer(files, many=True)
        paginator = UploadFilePagination()
        page_user_list = paginator.paginate_queryset(file_serializer.data, self.request, view=self)
        return paginator.get_paginated_response(page_user_list)

    def post(self, request, *args, **kwargs):
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
        file = self.get_object(pk)
        serializer = UploadFileSerializer(file)
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        file = self.get_object(pk)
        file.delete()
        default_storage.delete(f"{settings.MEDIA_ROOT}/upload/{file.file_name}")
        return Response(f'{file.file_name} delete OK')
