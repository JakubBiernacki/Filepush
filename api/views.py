from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import FileSerializer, ShareDirSerializer
from .models import Sharedir, File
from rest_framework.decorators import action


# Create your views here.


class FileViewSet(viewsets.ViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):

        if files := request.FILES:

            dir = Sharedir.objects.create(user=request.user)
            print(files)

            to_create = []
            for f in files.values():
                p = File(dir=dir, file=f)

                to_create.append(p)

            File.objects.bulk_create(to_create)

            return Response({'link': reverse('dashboard')}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShareDirViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Sharedir.objects.all()
    serializer_class = ShareDirSerializer
    lookup_field = 'code'

    @action(detail=True, methods=['get'])
    def files(self, request, code=None):
        queryset = get_object_or_404(Sharedir, code=code).file_set.all()

        serializer = FileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
