import threading


class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except AttributeError:
            return None


class MultithreadingBert:
    def __init__(self, model, question, context, thread_number):
        self.model = model
        self.question = question
        self.context = context
        self.thread_number = thread_number

    def run_threads(self):
        context = self.split_context()
        threads = []

        for i in range(self.thread_number):
            args = (context.get(i),)
            thread = MyThread(func=self.execute_function, args=args)
            threads.append(thread)
            thread.start()

        results = []
        for thread in threads:
            thread.join()
            results.append(thread.get_result())

        return self.evaluate_result(results)

    def execute_function(self, context):
        return self.model.fit(self.question, context)

    def evaluate_result(self, results) -> str:
        return max(results, key=lambda x: x['score']).get('answer')

    def split_context(self):
        index = int(len(self.context) / self.thread_number)
        split_result = {}
        start = 0
        end = index
        for i in range(self.thread_number):
            split_result[i] = self.context[start:end]
            start += index
            end += index
        return split_result
