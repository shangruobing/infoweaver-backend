from .filters import NoticeFilterBackend
from .utils.str2date_range import str_date_range
from .models import Notice
from rest_framework import status
from rest_framework.exceptions import APIException
from py2neo import Graph
import py2neo
import jieba
import jieba.posseg as pseg
import difflib
from django.conf import settings

try:
    jieba.load_userdict(r'..\public\dictionary.txt')
    with open(r'..\public\mydict.txt', encoding='UTF-8') as dict_file:
        myDict = dict_file.readlines()
        print("Custom file dictionary loaded successfully")
except Exception:
    raise APIException("Custom file dictionary loading failed")

try:
    jieba.enable_paddle()
except Exception:
    raise APIException("Paddle loading failed")

try:
    config = settings.DATABASES.get("neo4j")
    graph = Graph(config.get("HOST"), auth=(config.get("USER"), config.get("PASSWORD")))
    print("Neo4j graph database connected successfully")
except py2neo.errors.ConnectionUnavailable:
    raise APIException("Neo4j graph database connection failed", code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Question:
    def __init__(self, question):
        self.question = question

    def init_query_function(self):
        dictResult = difflib.get_close_matches(self.question, myDict, 1, cutoff=0.8)
        if dictResult:
            print("根据自定义字典查询MySQL")
            notices = Notice.objects.filter(name__icontains=dictResult[0][:-5])
        else:
            print("自定义字典查询失败 进行Neo4j查询")
            id_list = self.execute_neo4j_query(self.question)
            notices = Notice.objects.filter(file_id__in=id_list)

        return notices

    def execute_neo4j_query(self, question: str) -> []:
        """
        输入一个问题字符串，返回查询到的文件ID列表
        :param question: 需要查询的问题
        :return: 查询结果的文件ID列表
        """
        sql_list = self.search_by_jieba(question)
        neo_list = self.search_by_paddle(question)
        print("jieba查询结果", sql_list)
        print("Paddle查询结果", neo_list)
        id_list = []
        if sql_list and neo_list:
            id_list = set(sql_list).intersection(set(neo_list))
            print("jieba & Paddle结果交集", id_list)
        elif sql_list:
            id_list = sql_list
            print('jieba结果集 Paddle结果为空', id_list)
        elif neo_list:
            id_list = neo_list
            print("Paddle结果集 jieba结果为空", id_list)
        return id_list

    def search_by_jieba(self, question: str) -> []:
        """
        根据自定义Event字典，使用jieba的分词，返回符合条件的文件ID列表
        :param question: 需要查询的问题
        :return: 文件ID列表
        """
        jieba_words = pseg.cut(question, use_paddle=False)
        print("jieba识别开始")
        for i, flag in jieba_words:
            print(i, flag)
            if flag == "event":
                print("jieba识别一个自定义的Event Label", i)
                queryset = Notice.objects.filter(label__icontains=i)
                id_list = [i.file_id for i in queryset]
                return id_list

    def search_by_paddle(self, question: str) -> []:
        """
        根据问题，通过日期查找MySQL或者根据生成Cypher语句查询Neo4j返回一个文件id列表
        :param question:需要查询的问题
        :return:查询结果的文件ID列表
        """
        id_list = self.search_by_date(question)
        if id_list:
            return id_list
        condition = self.get_cypher_condition(question)
        cypher = self.get_cypher(condition)
        print("Cypher", cypher)
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
        print("时间识别开始")
        id_list = []
        for question, flag in words:
            print(question, flag)
            if flag == 'TIME' and question in ["去年", "今年", "明年",
                                               "上个月", "本月", "下个月",
                                               "上周", "本周", "下周",
                                               "昨天", "今天", "明天"]:
                print("进入了MySQL的日期范围匹配")
                id_list = self.execute_date_filter(str_date=question)
                break
        return id_list

    def get_cypher_condition(self, question: str) -> []:
        """
        根据问题，用百度Paddle语义识别，返回语义识别的结果列表
        :param question:需要查询的问题
        :return:语义识别的结果列表
        """
        words = pseg.cut(question, use_paddle=True)
        condition = []
        nodes_label = {
            "TIME": "time",
            "LOC": "location",
            "ORG": "org",
            "PER": "person"
        }
        print("Paddle识别开始")
        for question, flag in words:
            print(question, flag)
            try:
                condition.append({'question_type': nodes_label[flag], 'question': question})
            except KeyError as e:
                print("KeyError", e)
                continue
        return condition

    def execute_date_filter(self, str_date: str) -> []:
        """
            时间过滤调用函数，通过调用utils/str_date_range.py函数实现Django的日期查询
            输入一个日期字符串 例如 明天 后天 上一个
            返回查询的ID列表
            """
        start_date, end_date = str_date_range(str_date)
        notices = Notice.objects.all()
        notice_filter = NoticeFilterBackend()
        id_list = notice_filter.date_filter(notices, start_date=start_date, end_date=end_date)
        print("时间过滤器", id_list)
        return id_list

    def get_cypher(self, condition: []) -> str:
        cypher = ""
        if len(condition) == 1:
            cypher = f'match(n:{condition[0]["question_type"]})-[*2]-(answer:Title) where n.name contains "{condition[0]["question"]}" return answer,id(answer)'
        elif len(condition) == 2:
            cypher = f'match(n:{condition[0]["question_type"]})-[*2]-(answer:Title) where n.name contains "{condition[0]["question"]}" with answer match (answer)-[*2]-(s:{condition[1]["question_type"]}) where s.name contains "{condition[1]["question"]}" return answer,id(answer)'
        elif len(condition) == 3:
            cypher = f'match(n:{condition[0]["question_type"]})-[*2]-(answer:Title) where n.name contains "{condition[0]["question"]}" with answer match (answer)-[*2]-(s:{condition[1]["question_type"]}) where s.name contains "{condition[1]["question"]}" with answer match (answer)-[*2]-(c:{condition[2]["question_type"]}) where c.name contains "{condition[2]["question"]}" return answer,id(answer) '
        elif len(condition) == 4:
            cypher = f'match(n:{condition[0]["question_type"]})-[*2]-(answer:Title) where n.name contains "{condition[0]["question"]}" with answer match (answer)-[*2]-(s:{condition[1]["question_type"]}) where s.name contains "{condition[1]["question"]}" with answer match (answer)-[*2]-(c:{condition[2]["question_type"]}) where c.name contains "{condition[2]["question"]}" with answer match (answer)-[*2]-(d:{condition[3]["question_type"]}) where d.name contains "{condition[3]["question"]}" return answer,id(answer)'
        return cypher
