import abc
from abc import ABC

import jieba
import jieba.posseg as pseg
from django.conf import settings

from .cypher import Cypher
from QAS.models import Notice
from QAS.utils.db_conntcion import getGraphInstance
from QAS.filters import NoticeFilterBackend
from QAS.utils.str2date import str_date_range

try:
    jieba.load_userdict(settings.STATIC_ROOT + '/dictionary/custom_event.txt')
    print("Custom label dictionary loaded successfully")
except Exception:
    raise RuntimeError("Custom file dictionary loading failed")

try:
    graph = getGraphInstance()
except Exception:
    raise RuntimeError("Neo4j graph database connection failed")


class Query(ABC):
    def __init__(self, question):
        self.question = question

    @abc.abstractmethod
    def execute_query(self) -> []:
        pass

    def __str__(self):
        return f"The query's question:{self.question}"

    __repr__ = __str__


class JiebaQuery(Query):
    def __init__(self, question):
        super(JiebaQuery, self).__init__(question)

    def execute_query(self) -> []:
        """
        根据自定义Event字典，使用jieba的分词，返回符合条件的文件ID列表
        :return: 文件ID列表
        """
        jieba_words = pseg.cut(self.question, use_paddle=False)
        for i, flag in jieba_words:
            if flag == "event":
                queryset = Notice.objects.filter(label__icontains=i)
                id_list = [i.file_id for i in queryset]
                return id_list


class PaddleQuery(Query):
    def __init__(self, question):
        super(PaddleQuery, self).__init__(question)

    def execute_query(self) -> []:
        """
        根据问题，通过日期查找MySQL或者根据生成Cypher语句查询Neo4j返回一个文件id列表
        """
        id_list = self.search_by_date(self.question)
        if id_list:
            return id_list

        cypher = Cypher(self.question).get_cypher()
        answer = graph.run(cypher).data()
        id_list = [i['id(answer)'] for i in answer]
        return id_list

    def search_by_date(self, question: str) -> []:
        """
        根据日期范围，查询MySQL数据库，返回一个文件id列表
        :param question:需要查询的问题
        :return:查询结果的文件ID列表
        """
        words = pseg.cut(question, use_paddle=True)
        id_list = []
        for question, flag in words:
            if flag == 'TIME' and question in ["去年", "今年", "明年",
                                               "上个月", "本月", "下个月",
                                               "上周", "本周", "下周",
                                               "昨天", "今天", "明天"]:
                id_list = DateQuery(question).execute_query()
                break
        return id_list


class DateQuery(Query):
    def __init__(self, question):
        super(DateQuery, self).__init__(question)

    def execute_query(self) -> []:
        """
        时间过滤调用函数，通过调用utils/str_date_range.py函数实现Django的日期查询
        输入一个日期字符串 例如 明天 后天 上一个
        返回查询的ID列表
        """
        start_date, end_date = str_date_range(self.question)
        notices = Notice.objects.all()
        notice_filter = NoticeFilterBackend()
        id_list = notice_filter.date_filter(notices, start_date=start_date, end_date=end_date)
        return id_list
