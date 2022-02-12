from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedRelatedField(many=True, view_name='notice-detail', read_only=True)
    mysql_id = serializers.CharField(source="id")
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Notice
        fields = "__all__"
        read_only_fields = ['id']
