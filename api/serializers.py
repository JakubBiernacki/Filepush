from .models import File, Sharedir
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file',)


class ShareDirSerializer(serializers.ModelSerializer):

    link = serializers.HyperlinkedIdentityField(view_name='dir', lookup_field='code', read_only=True)
    class Meta:
        model = Sharedir
        fields = ('id', 'code', 'link')

