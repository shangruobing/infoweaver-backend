import difflib
from django.conf import settings
from rest_framework.exceptions import APIException

from QAS.models import Notice
from .query import JiebaQuery, PaddleQuery
from ..utils.baidu_search import baidu_search
from ..utils import answer_type

try:
    with open(settings.STATIC_ROOT + '/dictionary/notice.txt', encoding='UTF-8') as dict_file:
        notice_dict = dict_file.readlines()
        print("Custom filename dictionary loaded successfully")

except Exception:
    raise APIException("Custom file dictionary loading failed")


class Question:
    def __init__(self, question):
        self.question = question

    def __str__(self):
        return f"Question:{self.question}"

    def get_query_results(self):
        matched_result = difflib.get_close_matches(self.question, notice_dict, 1, cutoff=0.8)
        if matched_result:
            notices = Notice.objects.filter(name__icontains=matched_result[0][:-5])
            return answer_type.LOCAL, notices

        else:
            id_list = self.execute_query(self.question)
            notices = Notice.objects.filter(file_id__in=id_list)

            if notices:
                return answer_type.DATABASE, notices

            else:
                answer = baidu_search(self.question)
                if len(answer) != 0:
                    return answer_type.BAIDU, answer

        return answer_type.UNKNOWN, None

    def execute_query(self, question: str) -> []:
        """
        输入一个问题字符串，返回查询到的文件ID列表
        :param question: 需要查询的问题
        :return: 查询结果的文件ID列表
        """
        sql_list = JiebaQuery(question).execute_query()
        neo_list = PaddleQuery(question).execute_query()

        id_list = []
        if sql_list and neo_list:
            id_list = set(sql_list).intersection(set(neo_list))
        elif sql_list:
            id_list = sql_list
        elif neo_list:
            id_list = neo_list
        return id_list
