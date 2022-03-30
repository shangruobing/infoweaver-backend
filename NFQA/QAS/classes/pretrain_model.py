from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline


class BertModel:
    def __init__(self):
        self.model = self.__init_model()

    def __init_model(self):
        model = AutoModelForQuestionAnswering.from_pretrained('uer/roberta-base-chinese-extractive-qa')
        tokenizer = AutoTokenizer.from_pretrained('uer/roberta-base-chinese-extractive-qa')
        return pipeline('question-answering', model=model, tokenizer=tokenizer)

    def fit(self, question, context):
        parameters = {'question': question, 'context': context}
        results = self.model(parameters)
        return results
