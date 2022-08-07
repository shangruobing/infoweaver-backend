import csv

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from ..pagination import GenericPagination


class CorpusListView(APIView):

    def get(self, request, *args, **kwargs):
        """
        查询语料库
        """
        with open(settings.STATIC_ROOT + '/dictionary/daily_chat.csv', "r", encoding='UTF-8') as corpus_file:
            reader = csv.DictReader(corpus_file)
            corpus = [i for i in reader]
            paginator = GenericPagination()
            page_user_list = paginator.paginate_queryset(corpus, self.request, view=self)
            return paginator.get_paginated_response(page_user_list)

    def post(self, request, *args, **kwargs):
        question = request.data.get("question")
        answer = request.data.get("answer")
        data = [question, answer]

        with open(settings.STATIC_ROOT + '/dictionary/daily_chat.csv', "a", encoding='UTF-8') as corpus_csv:
            writer = csv.writer(corpus_csv)
            writer.writerow(data)
            return Response(f'Add {data} OK')
