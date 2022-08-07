from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..classes.question import Question

from ..utils import answer_type
from ..classes.query import graph
from ..classes.chat import ChatManager
from ..serializers import NoticeSerializer
from ..utils.threads import MultithreadingBert
from ..pagination import NoticePagination

try:
    # Warning!!!
    model = None
    # model = BertModel()
    print("BERT model loaded successfully")
except Exception:
    raise RuntimeError("BERT model load failed")


class Neo4jView(APIView):
    def get(self, request, pk, *args, **kwargs):
        """
        根据图数据库中的文件id查询这个文件的标题
        本方法是测试数据库连通性时候使用
        :param request: 请求
        :param pk: 文件ID
        """
        cypher = f"match (n:Title)-[*2]-(t:abstract) where id(n)={pk} unwind t.name as answer return answer"
        answer = graph.run(cypher).data()
        result = [i['answer'] for i in answer]
        return Response(result)

    def post(self, request, *args, **kwargs):
        """
        本方法是问答机器人的主方法
        通过文件名匹配->Neo4j->百度百科的顺序依次进行查询
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
