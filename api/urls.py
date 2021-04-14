from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('file', FileViewSet, basename='file')
router.register('sharedir', ShareDirViewSet, basename='sharedir')

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('', include(router.urls)),
]
