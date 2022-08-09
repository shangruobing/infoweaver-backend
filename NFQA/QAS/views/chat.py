from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from ..classes.question import Question
from ..classes.pretrained_model import BertModel
from ..utils import answer_type
from ..classes.query import graph
from ..classes.chat import ChatManager
from ..serializers import NoticeSerializer
from ..utils.threads import MultithreadingBert
from ..pagination import NoticePagination

try:
    if not settings.ENABLE_BERT:
        model = None
        print("BERT Not Enabled")
    else:
        model = BertModel()
        print("BERT model loaded successfully")
except Exception:
    raise RuntimeError("BERT model load failed")


class Neo4jView(APIView):
    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve the title of the file based on the file ID in the graph database.
        This method is used when testing database connectivity.
        """
        cypher = f"match (n:Title)-[*2]-(t:abstract) where id(n)={pk} unwind t.name as answer return answer"
        answer = graph.run(cypher).data()
        result = [i['answer'] for i in answer]
        return Response(result)

    def post(self, request, *args, **kwargs):
        """
        Question answering robot.
        Search by file name match -> Neo4j -> Baidu Encyclopedia.
        """
        try:
            question = request.data['question']
            print(request.data)

            chatManager = ChatManager(question)
            reply_type, reply = chatManager.get_reply()

            if reply:
                return Response({"answer_type": reply_type, "results": reply})

            has_history = request.data.get('has_history', False)

            if has_history:
                history = request.data.get('history')
                file_id = history.get('file_id', '')
                cypher = f"match (title)-[]-(context:File) where id(title)={file_id} return context.name"
                context = graph.run(cypher).data()[0].get("context.name", "")
                context = ''.join(context.split()).strip()
                result = MultithreadingBert(model, question, context, thread_number=8).run_threads()
                return Response({"answer_type": answer_type.BERT, "results": result})

            else:
                question_object = Question(question)
                result_type, result = question_object.get_query_results()

                if result_type in (answer_type.DATABASE, answer_type.LOCAL):
                    serializer = NoticeSerializer(result, many=True, context={'request': request})
                    paginator = NoticePagination()
                    page_user_list = paginator.paginate_queryset(serializer.data, self.request, view=self)
                    return paginator.get_paginated_response(page_user_list)

                else:
                    return Response({"answer_type": result_type, "results": result})
        except Exception:
            return Response({"answer_type": answer_type.UNKNOWN, "results": None})

    def put(self, request, *args, **kwargs):
        """
        Multi-thread Bert model.
        This is a test method.
        """
        try:
            question = request.data['question']
            file_id = request.data['id']

            thread_number = int(request.data['thread'])

            cypher = f"match (title)-[]-(context:File) where id(title)={file_id} return context.name"

            context = graph.run(cypher).data()[0].get("context.name", "")
            context = ''.join(context.split()).strip()
            if thread_number > 1:
                result = MultithreadingBert(model, question, context, thread_number).run_threads()
            else:
                result = model.fit(question, context)

            return Response(result)
        except (IndexError, KeyError):
            return Response('ERROR!', status=status.HTTP_400_BAD_REQUEST)
