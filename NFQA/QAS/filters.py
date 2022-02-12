import time
from rest_framework import filters
from datetime import datetime


class NoticeFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date is not None or end_date is not None:

            try:
                start_date = datetime.strptime(start_date, '%Y%m%d')
            except (ValueError, TypeError):
                start_date = datetime.strptime("19700101", '%Y%m%d')
            try:
                end_date = datetime.strptime(end_date, '%Y%m%d')
            except (ValueError, TypeError):
                end_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            queryset = queryset.filter(date__range=(start_date, end_date))

        return queryset
