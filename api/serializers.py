from .models import File, Sharedir
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file',)


class ShareDirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharedir
        fields = '__all__'
