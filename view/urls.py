from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logout/', LogoutuserView.as_view(), name='logout'),
    path('dashboard/',DashboardView.as_view(), name='dashboard'),
    path('dashboard/adddir/',AdddirView.as_view(), name='adddir'),

    # path('', include('allauth.urls')),


]