from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from django.conf import settings

model_path = settings.STATIC_ROOT + "/models"


class BertModel:
    def __init__(self):
        self.model = self.__init_model()

    def __init_model(self):
        # Model name 'uer/roberta-base-chinese-extractive-qa'
        model = AutoModelForQuestionAnswering.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        return pipeline('question-answering', model=model, tokenizer=tokenizer)

    def fit(self, question, context):
        parameters = {'question': question, 'context': context}
        results = self.model(parameters)
        return results
