import csv
from django.conf import settings
from rest_framework.exceptions import APIException

from ..utils import answer_type


# try:
#     with open(settings.STATIC_ROOT + '/dictionary/daily_chat.csv', encoding='UTF-8') as corpus_file:
#         reader = csv.DictReader(corpus_file)
#         corpus = [dict(i) for i in reader]
#         print("Daily chat corpus loaded successfully")
#
# except Exception:
#     raise APIException("Custom file dictionary loading failed")


class ChatManager:
    def __init__(self, sentence):
        self.sentence = sentence

    def __str__(self):
        return f"Sentence:{self.sentence}"

    def get_reply(self):
        matched_result = self.execute_corpus_match(self.sentence)

        if matched_result:
            return answer_type.CHAT, matched_result

        return answer_type.UNKNOWN, None

    def load_corpus(self):
        with open(settings.STATIC_ROOT + '/dictionary/daily_chat.csv', "r", encoding='UTF-8') as corpus_file:
            reader = csv.DictReader(corpus_file)
            corpus = [dict(i) for i in reader]
            return corpus

    def execute_corpus_match(self, question: str) -> str:
        for i in self.load_corpus():
            if question == i["Question"]:
                return i["Answer"]
