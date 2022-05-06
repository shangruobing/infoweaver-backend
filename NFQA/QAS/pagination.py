from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .utils import answer_type


class GenericPagination(PageNumberPagination):
    # 默认每页显示的数据条数
    page_size = 10
    # 获取URL参数中设置的每页显示数据条数
    page_size_query_param = 'page_size'
    # 获取URL参数中传入的页码key
    page_query_param = 'page'
    # 最大支持的每页显示的数据条数
    max_page_size = 10


class NoticePagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('answer_type', answer_type.DATABASE),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))


class UploadFilePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 10
