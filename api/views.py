from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import FileSerializer, ShareDirSerializer
from .models import Sharedir, File, DownloadData
from rest_framework.decorators import action
from .mypermissions import IsOwnerOrReadOnly


# Create your views here.


class FileViewSet(viewsets.ViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):

        if files := request.FILES:
            user = request.user

            dir = Sharedir(user=user)
            print(files)

            to_create = []
            size = 0
            for f in files.values():
                p = File(dir=dir, file=f)
                size += f.size
                to_create.append(p)

            size = round(size / 1048576, 2)

            grupa = user.groups.values_list('name', flat=True)[0]

            if grupa == 'standard':
                if user.all_file_size + size > 10:
                    return Response({f"Brak miejsca - user w grupie \"{grupa}\" może "
                                     "udostępniać pliki do 10MB"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            elif grupa == 'premium':
                if user.all_file_size + size > 40:
                    return Response({f"Brak miejsca - user w grupie \"{grupa}\" może "
                                     "udostępniać pliki do 40MB"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            dir.size = size
            dir.save()
            File.objects.bulk_create(to_create)

            return Response({'link': reverse('dashboard')}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShareDirViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Sharedir.objects.all()
    serializer_class = ShareDirSerializer
    lookup_field = 'code'
    permission_classes = [IsOwnerOrReadOnly]

    @action(detail=True, methods=['get'])
    def files(self, request, code=None):
        queryset = get_object_or_404(Sharedir, code=code).file_set.all()

        serializer = FileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatisticsViewSet(viewsets.ViewSet):
    def list(self, request):
        files_count = File.objects.count()
        download_count = DownloadData.objects.count()

        return Response({'files_count': files_count, 'download_count': download_count}, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.user
        ip = request.META['REMOTE_ADDR']
        agent = request.META['HTTP_USER_AGENT']
        file = request.data.get('filename')

        DownloadData.objects.create(user=user, ip_address=ip, user_agent=agent, file=file)

        return Response(status=status.HTTP_201_CREATED)
