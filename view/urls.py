from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/',DashboardView.as_view(), name='dashboard'),
    path('dashboard/adddir/', AdddirView.as_view(), name='adddir'),

    path('sharedir/<str:code>/', ShareDirView.as_view(), name='dir'),

    # path('', include('allauth.urls')),


]