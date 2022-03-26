import jieba.posseg as pseg
import jieba
from rest_framework.exceptions import APIException

try:
    jieba.enable_paddle()
except Exception:
    raise APIException("Paddle loading failed")


class Cypher:
    def __init__(self, question: str):
        self.question = question

    def get_cypher(self):
        condition = self.get_cypher_condition(self.question)
        return self.generate_cypher(condition)

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

    def generate_cypher(self, condition: []) -> str:
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
