from rest_framework import serializers

from .models import Notice, UploadFile


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    mysql_id = serializers.CharField(source="id")
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Notice
        fields = "__all__"
        read_only_fields = ['id']


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'
