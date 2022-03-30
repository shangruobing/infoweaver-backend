import threading


class BertModelThread(threading.Thread):
    def __init__(self, model, question, context):
        threading.Thread.__init__(self)
        self.model = model
        self.question = question
        self.context = context
        self.result = None

    def run(self):
        self.result = self.model.fit(self.question, self.context)

    def get_result(self):
        return self.result


class MultithreadingBert:
    def __init__(self, model, question, context, number):
        self.model = model
        self.question = question
        self.context = context
        self.number = number
        self.result = None

    def split_context(self):
        index = int(len(self.context) / self.number)
        split_result = {}
        start = 0
        end = index
        for i in range(self.number):
            split_result[i] = self.context[start:end]
            start += index
            end += index
        return split_result

    def run_threads(self):
        context = self.split_context()
        threads = []
        results = []
        for i in range(6):
            threads.append(BertModelThread(self.model, self.question, context.get(i)))

        for i in threads:
            i.start()
        for i in threads:
            i.join()
            results.append(i.get_result())
        return results
