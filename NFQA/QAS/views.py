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
import re
import requests
from bs4 import BeautifulSoup
from rest_framework import status
from .classes.question import Question
from .classes.query import graph


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
        print("question:", question)

        question_object = Question(question)
        notices = question_object.get_query_results()

        serializer = NoticeSerializer(notices, many=True, context={'request': request})
        if len(serializer.data) == 0:
            print("Neo4查询失败 百度百科查询")
            return Response(self.baidu_search(question))

        paginator = NoticePagination()
        page_user_list = paginator.paginate_queryset(serializer.data, self.request, view=self)
        return paginator.get_paginated_response(page_user_list)

    def baidu_search(self, word: str) -> str:
        """
        百度百科检索问题
        :param word: 需要查询的问题
        :return: 百度百科查询结果
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"
        }

        url = f'https://baike.baidu.com/item/{word}'
        response = requests.get(url=url, headers=headers, timeout=10)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'lxml')

        li_list = soup.select('.lemma-summary')

        results = [re.sub(r'\[[0-9 \-]+]', '', i.text).strip() for i in li_list]
        result = ''.join(results)
        if len(result) > 100:
            result = result[:100] + "……"
        return result
